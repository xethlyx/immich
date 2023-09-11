//
// AUTO-GENERATED FILE, DO NOT MODIFY!
//
// @dart=2.12

// ignore_for_file: unused_element, unused_import
// ignore_for_file: always_put_required_named_parameters_first
// ignore_for_file: constant_identifier_names
// ignore_for_file: lines_longer_than_80_chars

part of openapi.api;

class CLIPConfig {
  /// Returns a new [CLIPConfig] instance.
  CLIPConfig({
    this.embeddingId,
    required this.enabled,
    this.indexName,
    this.k,
    this.mode,
    required this.modelName,
    this.modelType,
  });

  ///
  /// Please note: This property should have been non-nullable! Since the specification file
  /// does not include a default value (using the "default:" property), however, the generated
  /// source code must fall back to having a nullable type.
  /// Consider adding a "default:" property in the specification file to hide this note.
  ///
  String? embeddingId;

  bool enabled;

  ///
  /// Please note: This property should have been non-nullable! Since the specification file
  /// does not include a default value (using the "default:" property), however, the generated
  /// source code must fall back to having a nullable type.
  /// Consider adding a "default:" property in the specification file to hide this note.
  ///
  String? indexName;

  ///
  /// Please note: This property should have been non-nullable! Since the specification file
  /// does not include a default value (using the "default:" property), however, the generated
  /// source code must fall back to having a nullable type.
  /// Consider adding a "default:" property in the specification file to hide this note.
  ///
  num? k;

  ///
  /// Please note: This property should have been non-nullable! Since the specification file
  /// does not include a default value (using the "default:" property), however, the generated
  /// source code must fall back to having a nullable type.
  /// Consider adding a "default:" property in the specification file to hide this note.
  ///
  CLIPMode? mode;

  String modelName;

  ///
  /// Please note: This property should have been non-nullable! Since the specification file
  /// does not include a default value (using the "default:" property), however, the generated
  /// source code must fall back to having a nullable type.
  /// Consider adding a "default:" property in the specification file to hide this note.
  ///
  ModelType? modelType;

  @override
  bool operator ==(Object other) => identical(this, other) || other is CLIPConfig &&
     other.embeddingId == embeddingId &&
     other.enabled == enabled &&
     other.indexName == indexName &&
     other.k == k &&
     other.mode == mode &&
     other.modelName == modelName &&
     other.modelType == modelType;

  @override
  int get hashCode =>
    // ignore: unnecessary_parenthesis
    (embeddingId == null ? 0 : embeddingId!.hashCode) +
    (enabled.hashCode) +
    (indexName == null ? 0 : indexName!.hashCode) +
    (k == null ? 0 : k!.hashCode) +
    (mode == null ? 0 : mode!.hashCode) +
    (modelName.hashCode) +
    (modelType == null ? 0 : modelType!.hashCode);

  @override
  String toString() => 'CLIPConfig[embeddingId=$embeddingId, enabled=$enabled, indexName=$indexName, k=$k, mode=$mode, modelName=$modelName, modelType=$modelType]';

  Map<String, dynamic> toJson() {
    final json = <String, dynamic>{};
    if (this.embeddingId != null) {
      json[r'embedding_id'] = this.embeddingId;
    } else {
    //  json[r'embedding_id'] = null;
    }
      json[r'enabled'] = this.enabled;
    if (this.indexName != null) {
      json[r'index_name'] = this.indexName;
    } else {
    //  json[r'index_name'] = null;
    }
    if (this.k != null) {
      json[r'k'] = this.k;
    } else {
    //  json[r'k'] = null;
    }
    if (this.mode != null) {
      json[r'mode'] = this.mode;
    } else {
    //  json[r'mode'] = null;
    }
      json[r'modelName'] = this.modelName;
    if (this.modelType != null) {
      json[r'modelType'] = this.modelType;
    } else {
    //  json[r'modelType'] = null;
    }
    return json;
  }

  /// Returns a new [CLIPConfig] instance and imports its values from
  /// [value] if it's a [Map], null otherwise.
  // ignore: prefer_constructors_over_static_methods
  static CLIPConfig? fromJson(dynamic value) {
    if (value is Map) {
      final json = value.cast<String, dynamic>();

      return CLIPConfig(
        embeddingId: mapValueOfType<String>(json, r'embedding_id'),
        enabled: mapValueOfType<bool>(json, r'enabled')!,
        indexName: mapValueOfType<String>(json, r'index_name'),
        k: json[r'k'] == null
            ? null
            : num.parse(json[r'k'].toString()),
        mode: CLIPMode.fromJson(json[r'mode']),
        modelName: mapValueOfType<String>(json, r'modelName')!,
        modelType: ModelType.fromJson(json[r'modelType']),
      );
    }
    return null;
  }

  static List<CLIPConfig> listFromJson(dynamic json, {bool growable = false,}) {
    final result = <CLIPConfig>[];
    if (json is List && json.isNotEmpty) {
      for (final row in json) {
        final value = CLIPConfig.fromJson(row);
        if (value != null) {
          result.add(value);
        }
      }
    }
    return result.toList(growable: growable);
  }

  static Map<String, CLIPConfig> mapFromJson(dynamic json) {
    final map = <String, CLIPConfig>{};
    if (json is Map && json.isNotEmpty) {
      json = json.cast<String, dynamic>(); // ignore: parameter_assignments
      for (final entry in json.entries) {
        final value = CLIPConfig.fromJson(entry.value);
        if (value != null) {
          map[entry.key] = value;
        }
      }
    }
    return map;
  }

  // maps a json object with a list of CLIPConfig-objects as value to a dart map
  static Map<String, List<CLIPConfig>> mapListFromJson(dynamic json, {bool growable = false,}) {
    final map = <String, List<CLIPConfig>>{};
    if (json is Map && json.isNotEmpty) {
      // ignore: parameter_assignments
      json = json.cast<String, dynamic>();
      for (final entry in json.entries) {
        map[entry.key] = CLIPConfig.listFromJson(entry.value, growable: growable,);
      }
    }
    return map;
  }

  /// The list of required keys that must be present in a JSON.
  static const requiredKeys = <String>{
    'enabled',
    'modelName',
  };
}

