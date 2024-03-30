import 'package:flutter/material.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import 'package:immich_mobile/modules/search/models/search_filter.dart';
import 'package:immich_mobile/shared/models/asset.dart';
import 'package:immich_mobile/shared/providers/api.provider.dart';
import 'package:immich_mobile/shared/providers/db.provider.dart';
import 'package:immich_mobile/shared/services/api.service.dart';
import 'package:isar/isar.dart';
import 'package:openapi/api.dart';

final searchServiceProvider = Provider(
  (ref) => SearchService(
    ref.watch(apiServiceProvider),
    ref.watch(dbProvider),
  ),
);

class SearchService {
  final ApiService _apiService;
  final Isar _db;

  SearchService(this._apiService, this._db);

  Future<List<String>?> getUserSuggestedSearchTerms() async {
    try {
      return await _apiService.assetApi.getAssetSearchTerms();
    } catch (e) {
      debugPrint("[ERROR] [getUserSuggestedSearchTerms] ${e.toString()}");
      return [];
    }
  }

  Future<List<String>?> getSearchSuggestions(
    SearchSuggestionType type, {
    String? country,
    String? state,
    String? make,
    String? model,
  }) async {
    try {
      return await _apiService.searchApi.getSearchSuggestions(
        type,
        country: country,
        state: state,
        make: make,
        model: model,
      );
    } catch (e) {
      debugPrint("[ERROR] [getSearchSuggestions] ${e.toString()}");
      return [];
    }
  }

  Future<List<Asset>?> search(SearchFilter filter, int page) async {
    try {
      SearchResponseDto? response;
      AssetTypeEnum? type;
      if (filter.mediaType == AssetType.image) {
        type = AssetTypeEnum.IMAGE;
      } else if (filter.mediaType == AssetType.video) {
        type = AssetTypeEnum.VIDEO;
      }

      if (filter.context != null && filter.context!.isNotEmpty) {
        response = await _apiService.searchApi.searchSmart(
          SmartSearchDto(
            query: filter.context!,
            country: filter.location.country,
            state: filter.location.state,
            city: filter.location.city,
            make: filter.camera.make,
            model: filter.camera.model,
            takenAfter: filter.date.takenAfter,
            takenBefore: filter.date.takenBefore,
            isArchived: filter.display.isArchive,
            isFavorite: filter.display.isFavorite,
            isNotInAlbum: filter.display.isNotInAlbum,
            personIds: filter.people.map((e) => e.id).toList(),
            type: type,
            page: page,
          ),
        );
      } else {
        response = await _apiService.searchApi.searchMetadata(
          MetadataSearchDto(
            originalFileName: filter.filename,
            country: filter.location.country,
            state: filter.location.state,
            city: filter.location.city,
            make: filter.camera.make,
            model: filter.camera.model,
            takenAfter: filter.date.takenAfter,
            takenBefore: filter.date.takenBefore,
            isArchived: filter.display.isArchive,
            isFavorite: filter.display.isFavorite,
            isNotInAlbum: filter.display.isNotInAlbum,
            personIds: filter.people.map((e) => e.id).toList(),
            type: type,
            page: page,
          ),
        );
      }

      if (response == null) {
        return null;
      }

      return _db.assets
          .getAllByRemoteId(response.assets.items.map((e) => e.id));
    } catch (error) {
      debugPrint("Error [search] $error");
    }
    return null;
  }

  Future<List<Asset>?> searchAsset(
    String searchTerm, {
    bool smartSearch = true,
  }) async {
    // TODO search in local DB: 1. when offline, 2. to find local assets
    try {
      final SearchResponseDto? results = await _apiService.searchApi.search(
        query: searchTerm,
        smart: smartSearch,
      );
      if (results == null) {
        return null;
      }
      // TODO local DB might be out of date; add assets not yet in DB?
      return _db.assets.getAllByRemoteId(results.assets.items.map((e) => e.id));
    } catch (e) {
      debugPrint("[ERROR] [searchAsset] ${e.toString()}");
      return null;
    }
  }

  Future<List<CuratedLocationsResponseDto>?> getCuratedLocation() async {
    try {
      var locations = await _apiService.assetApi.getCuratedLocations();

      return locations;
    } catch (e) {
      debugPrint("Error [getCuratedLocation] ${e.toString()}");
      return [];
    }
  }

  Future<List<CuratedObjectsResponseDto>?> getCuratedObjects() async {
    try {
      return await _apiService.assetApi.getCuratedObjects();
    } catch (e) {
      debugPrint("Error [getCuratedObjects] ${e.toString()}");
      return [];
    }
  }
}
