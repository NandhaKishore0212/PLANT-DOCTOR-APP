import 'package:flutter/foundation.dart';

class ApiConfig {
  // Permanent Cloud Backend URL — works anywhere (4G, 5G, WiFi) without Mac running
  static const String _publicTunnelUrl = "https://plant-doctor-backend-production-6566.up.railway.app";

  static String get baseUrl {
    if (kIsWeb) {
      final base = Uri.base;
      if (base.host == 'localhost' || base.host == '127.0.0.1') {
        return "http://${base.host}:${base.port}/api/v1";
      }
      final portStr = (base.port == 80 || base.port == 443 || base.port == 0) ? "" : ":${base.port}";
      return "${base.scheme}://${base.host}$portStr/api/v1";
    }
    // Mobile: uses public tunnel URL — works on any network!
    return "$_publicTunnelUrl/api/v1";
  }
}