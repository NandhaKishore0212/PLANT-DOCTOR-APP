import 'package:flutter/foundation.dart';

class ApiConfig {
  // Permanent Railway Cloud Backend — works on mobile & web from anywhere
  static const String _cloudBackendUrl = "https://plant-doctor-backend-production-6566.up.railway.app";

  static String get baseUrl {
    if (kIsWeb) {
      final base = Uri.base;
      // Only use local server when running on localhost (dev mode)
      if (base.host == 'localhost' || base.host == '127.0.0.1') {
        return "http://${base.host}:${base.port}/api/v1";
      }
      // For GitHub Pages or any other hosting — use Railway cloud backend
      return "$_cloudBackendUrl/api/v1";
    }
    // Mobile: always uses Railway cloud backend
    return "$_cloudBackendUrl/api/v1";
  }
}