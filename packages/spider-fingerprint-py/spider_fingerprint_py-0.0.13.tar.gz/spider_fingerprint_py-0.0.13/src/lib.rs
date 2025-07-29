use pyo3::prelude::*;
use pyo3::types::PyDict;

use spider_fingerprint::{
  configs::Tier,
  emulate, emulate_headers,
  http::{HeaderMap, HeaderName},
  spoof_viewport::{get_random_viewport, Viewport},
  url::Url,
  EmulationConfiguration, Fingerprint,
};

#[pyclass]
#[derive(Clone)]
pub struct PyViewport {
  /// Viewport screen width in pixels.
  #[pyo3(get, set)]
  pub width: u32,
  /// Viewport screen height in pixels.
  #[pyo3(get, set)]
  pub height: u32,
  /// Device scale factor (e.g. retina displays). `None` means no specific scaling factor.
  #[pyo3(get, set)]
  pub device_scale_factor: Option<f64>,
  /// Whether the viewport is emulating a mobile device.
  #[pyo3(get, set)]
  pub emulating_mobile: bool,
  /// Whether the viewport is in landscape orientation (`true`) or portrait (`false`).
  #[pyo3(get, set)]
  pub is_landscape: bool,
  /// Whether the viewport emulation supports touch-screen interactions.
  #[pyo3(get, set)]
  pub has_touch: bool,
}

#[pymethods]
impl PyViewport {
  #[new]
  pub fn new(width: u32, height: u32) -> Self {
    Self {
      width,
      height,
      device_scale_factor: None,
      emulating_mobile: false,
      is_landscape: false,
      has_touch: false,
    }
  }

  #[staticmethod]
  pub fn random() -> Self {
    let vp = get_random_viewport();
    Self {
      width: vp.width,
      height: vp.height,
      device_scale_factor: vp.device_scale_factor,
      emulating_mobile: vp.emulating_mobile,
      is_landscape: vp.is_landscape,
      has_touch: vp.has_touch,
    }
  }
}

/// The level of stealth applied in browser fingerprint emulation.
///
/// Controls how aggressively fingerprint protections are enforced during browser emulation.
/// This setting affects performance and stealth accuracy trade-offs for automated testing.
#[pyclass(eq, eq_int)]
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum PyTier {
  /// Basic spoofing protections.
  Basic,
  /// Basic spoofing including console output (allows developer tools logging).
  BasicWithConsole,
  /// Basic spoofing protections, but without WebGL spoofing.
  BasicNoWebgl,
  /// Mid-level spoofing protections, better resilience against fingerprint detection.
  Mid,
  /// Highest level spoofing protections available, aggressively targeting most fingerprinting techniques.
  Full,
  #[pyo3(name = "NoSpoof")]
  /// No spoofing or protections applied; raw fingerprint visible.
  None,
}

impl From<PyTier> for Tier {
  fn from(value: PyTier) -> Self {
    match value {
      PyTier::Basic => Tier::Basic,
      PyTier::BasicWithConsole => Tier::BasicWithConsole,
      PyTier::BasicNoWebgl => Tier::BasicNoWebgl,
      PyTier::Mid => Tier::Mid,
      PyTier::Full => Tier::Full,
      PyTier::None => Tier::None,
    }
  }
}

/// Fingerprint modes available for browser emulation.
///
/// Determines whether fingerprint protections include spoofing WebGL, GPU, or no fingerprint protections.
/// This influences how aggressively bot protections and fingerprinting methods might detect the browser session.
#[pyclass(eq, eq_int)]
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum PyFingerprintMode {
  /// Basic fingerprint mode, including WebGL and GPU attempts to spoof details.
  Basic,
  /// Native GPU, using real GPU-based fingerprint (for headless instances with real hardware).
  NativeGPU,
  #[pyo3(name = "NoSpoof")]
  /// No fingerprint spoofing, exposing actual browser fingerprint fully.
  None,
}

#[pyfunction(signature = (
    user_agent,
    tier,
    fingerprint_mode,
    dismiss_dialogs,
    viewport=None,
    eval_script=None
))]
/// Generate a JavaScript emulation script based on browser fingerprint settings and viewport configurations.
///
/// This emulation script integrates various spoofing techniques (fingerprint protection, webGL spoofing, GPU emulation, etc.) based on the provided parameters.
/// It can be injected (evaluated-on-new-document) into headless browsers or regular browser automation sessions to simulate realistic browsing profiles.
///
/// # Arguments
///
/// * `user_agent` - The full browser user agent string to emulate, used for spoofing HTTP headers and navigator details.
///
/// * `tier` - The stealth level (spoofing aggressiveness) defined by [`PyTier`].
///
/// * `fingerprint_mode` - Mode of browser fingerprint handling defined by [`PyFingerprintMode`].
///
/// * `dismiss_dialogs` - Automatically dismiss browser dialog prompts when set to `true`.
///
/// * `viewport` - Optional viewport screen configuration ([`PyViewport`]). Defines screen size, mobile emulation, device scale, and touch emulation.
///
/// * `eval_script` - Optional custom JavaScript code to inject and run alongside the generated spoofing scripts.
///
/// # Returns
///
/// * An `Option<String>` containing the generated JavaScript emulation script.
///   Returns `None` if no spoofing is required based on provided parameters.
pub fn generate_emulation_script(
  user_agent: &str,
  tier: PyTier,
  fingerprint_mode: PyFingerprintMode,
  dismiss_dialogs: bool,
  viewport: Option<&PyViewport>,
  eval_script: Option<&str>,
) -> PyResult<Option<String>> {
  let user_agent = if user_agent.is_empty() {
    ua_generator::ua::spoof_chrome_ua()
  } else {
    user_agent
  };

  let fingerprint = match fingerprint_mode {
    PyFingerprintMode::Basic => Fingerprint::Basic,
    PyFingerprintMode::NativeGPU => Fingerprint::NativeGPU,
    PyFingerprintMode::None => Fingerprint::None,
  };

  let mut config = EmulationConfiguration::setup_defaults(&user_agent);

  config.tier = tier.into();
  config.fingerprint = fingerprint;
  config.dismiss_dialogs = dismiss_dialogs;

  Ok(emulate(
    user_agent,
    &config,
    &viewport.map(|vp| Viewport {
      width: vp.width,
      height: vp.height,
      device_scale_factor: vp.device_scale_factor,
      emulating_mobile: vp.emulating_mobile,
      is_landscape: vp.is_landscape,
      has_touch: vp.has_touch,
    }),
    &eval_script.map(|s| Box::new(s.to_string())),
  ))
}

/// Emulate realistic HTTP Chrome browser headers.
///
/// This function generates a complete set of HTTP headers similar to those produced by a
/// Chrome web browser, tailored based on the given inputs.
///
/// # Parameters
///
/// - `user_agent` - A browser user-agent string to emulate.
/// - `header_map` - *(Optional)* A dictionary containing existing HTTP headers to seed the generation process.
///   These headers can override default values or supply additional ones.
/// - `hostname` - *(Optional)* The hostname of the domain making the request, used to produce accurate `Host` headers.
/// - `viewport` - *(Optional)* Dictionary specifying the viewport dimensions `{ "width": u32, "height": u32 }`.
///   Used to generate headers like "viewport-width".
/// - `domain_parsed` - *(Optional)* A parsed URL string representing the domain. This URL is used internally to
///   generate domain-specific header values. If the URL is invalid, this parameter is ignored.
///
/// # Returns
///
/// Returns a Python dictionary containing the emulated Chrome HTTP headers.
/// Always returns safely without throwing errors, even when provided invalid or incomplete input.
///
/// # Examples (Python)
///
/// ```python
/// from spider_fingerprint import generate_emulation_headers
///
/// headers = generate_emulation_headers(
///     user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
///     header_map={"Accept-Language": "en-US,en;q=0.9"},
///     hostname="example.com",
///     viewport={"width": 1920, "height": 1080},
///     domain_parsed="https://example.com"
/// )
///
/// print(headers)
/// ```
#[pyfunction(signature = (
    user_agent,
    header_map=None,
    hostname=None,
    viewport=None,
    domain_parsed=None
))]
pub fn generate_emulation_headers(
  py: Python,
  user_agent: &str,
  header_map: Option<Py<PyDict>>,
  hostname: Option<&str>,
  viewport: Option<Py<PyViewport>>,
  domain_parsed: Option<&str>,
) -> PyResult<PyObject> {
  let rust_header_map: Option<HeaderMap> = header_map.and_then(|hm| {
    let mut headers = HeaderMap::new();
    let hm_ref = hm.bind(py);

    for (key, value) in hm_ref.iter() {
      if let (Ok(key_str), Ok(val_str)) = (key.extract::<&str>(), value.extract::<&str>()) {
        if let (Ok(header_name), Ok(header_value)) =
          (key_str.parse::<HeaderName>(), val_str.parse())
        {
          headers.insert(header_name, header_value);
        }
      }
    }
    if headers.is_empty() {
      None
    } else {
      Some(headers)
    }
  });

  let rust_viewport: Option<Viewport> = viewport.and_then(|vp| {
    let vp_ref = vp.bind(py);
    let width = vp_ref
      .get_item("width")
      .and_then(|w| Ok(w.extract::<u32>().ok().unwrap_or_default()));
    let height = vp_ref
      .get_item("height")
      .and_then(|w| Ok(w.extract::<u32>().ok().unwrap_or_default()));

    match (width, height) {
      (Ok(width), Ok(height)) => {
        if width > 0 && height > 0 {
          Some(Viewport::new(width, height))
        } else {
          None
        }
      }
      _ => None,
    }
  });

  // Safely parsing domain_parsed URL, ignore invalid URL.
  let rust_domain_parsed: Option<Box<Url>> = domain_parsed
    .and_then(|url_str| Url::parse(url_str).ok())
    .map(Box::new);

  // Calling the underlying Rust function safely.
  let resulting_headers = emulate_headers(
    user_agent,
    &rust_header_map.as_ref(),
    &hostname,
    false, // adjust accordingly if needed
    &rust_viewport,
    &rust_domain_parsed,
  );

  let py_result_headers = PyDict::new(py);

  for (key, value) in resulting_headers.iter() {
    if let Ok(val_str) = value.to_str() {
      py_result_headers.set_item(key.as_str(), val_str).ok();
    }
  }

  Ok(py_result_headers.into())
}

/// Generate a random user-agent.
#[pyfunction]
pub fn spoof_ua_general() -> &'static str {
  ua_generator::ua::spoof_ua()
}

#[cfg(target_os = "macos")]
#[pyfunction]
/// Generate a random user-agent by platform.
pub fn spoof_ua() -> &'static str {
  ua_generator::ua::spoof_chrome_mac_ua()
}

#[cfg(target_os = "linux")]
#[pyfunction]
/// Generate a random user-agent by platform.
pub fn spoof_ua() -> &'static str {
  ua_generator::ua::spoof_chrome_linux_ua()
}

#[cfg(not(any(target_os = "macos", target_os = "linux")))]
#[pyfunction]
/// Generate a random user-agent by platform.
pub fn spoof_ua() -> &'static str {
  ua_generator::ua::spoof_chrome_ua()
}

#[pyfunction]
/// Generate playwright spoofs that help stealth.
pub fn spoof_playwright() -> &'static str {
  spider_fingerprint::spoofs::PW_INIT_SCRIPTS_SPOOF
}

#[pymodule]
fn spider_fingerprint_py(m: &Bound<'_, PyModule>) -> PyResult<()> {
  m.add_class::<PyViewport>()?;
  m.add_class::<PyTier>()?;
  m.add_class::<PyFingerprintMode>()?;
  m.add_function(wrap_pyfunction!(generate_emulation_script, m)?)?;
  m.add_function(wrap_pyfunction!(generate_emulation_headers, m)?)?;
  m.add_function(wrap_pyfunction!(spoof_ua, m)?)?;
  m.add_function(wrap_pyfunction!(spoof_ua_general, m)?)?;
  m.add_function(wrap_pyfunction!(spoof_playwright, m)?)?;

  Ok(())
}
