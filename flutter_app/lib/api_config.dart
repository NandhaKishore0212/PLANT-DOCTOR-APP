import 'package:flutter/foundation.dart';

class ApiConfig {
  // Your Mac's local IP address — mobile connects here over WiFi
  static const String _localBackendIp = "10.97.108.99";
  static const int _localBackendPort = 8080;

  static String get baseUrl {
    if (kIsWeb) {
      final base = Uri.base;
      // When serving from the backend itself (port 8080), use relative path
      if (base.host == 'localhost' || base.host == '127.0.0.1') {
        return "http://${base.host}:${base.port == 0 ? _localBackendPort : base.port}/api/v1";
      }
      final portStr = (base.port == 80 || base.port == 443 || base.port == 0) ? "" : ":${base.port}";
      return "${base.scheme}://${base.host}$portStr/api/v1";
    }
    // Mobile: connects to the same local Mac backend over WiFi
    // Make sure your phone is on the same WiFi network as your Mac!
    return "http://$_localBackendIp:$_localBackendPort/api/v1";
  }
}