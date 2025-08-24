
# 🔑 API ACCESS GUIDE FOR CONSERVATION DATABASES

## How to Resolve API Limitations

### 1. 🐦 eBird API (403 Forbidden)

**Problem:** eBird API requires authentication for most endpoints.

**Solution:**
1. **Get API Key:**
   - Visit: https://ebird.org/api/keygen
   - Create free eBird account
   - Request API key (instant approval)

2. **Usage:**
   ```python
   headers = {'X-eBirdApiToken': 'YOUR_API_KEY'}
   response = requests.get(url, headers=headers)
   ```

3. **Rate Limits:**
   - 100 requests per minute
   - No daily limit for most endpoints

### 2. 🔬 iNaturalist API (422 Unprocessable Entity)

**Problem:** Query parameters were invalid or conflicting.

**Solutions:**
1. **Fix Parameters:**
   ```python
   # Bad parameters that cause 422:
   params = {
       'place_id': 6927,
       'quality_grade': 'research',
       'has_photos': 'true',  # This might conflict
       'per_page': 200        # Too high for some queries
   }
   
   # Good parameters:
   params = {
       'place_id': 6927,
       'quality_grade': 'research',
       'per_page': 100
   }
   ```

2. **Alternative Endpoints:**
   - `/v1/observations/species_counts` - for species lists
   - `/v1/observations/identifiers` - for taxonomic data
   - `/v1/observations/observers` - for observer data

3. **No Authentication Required:** iNaturalist API is open!

### 3. 🦋 IUCN Red List API (404 Not Found)

**Problem:** Incorrect endpoint URLs or missing authentication.

**Solutions:**
1. **Get API Token:**
   - Visit: https://apiv3.iucnredlist.org/api/v3/token
   - Free registration required
   - Token provided instantly

2. **Correct Endpoints:**
   ```python
   # Correct base URL:
   base_url = "https://apiv3.iucnredlist.org/api/v3"
   
   # Country species:
   url = f"{base_url}/country/getspecies/MG"
   params = {'token': 'YOUR_TOKEN'}
   
   # Species details:
   url = f"{base_url}/species/{scientific_name}"
   ```

3. **Rate Limits:**
   - 10,000 requests per month (free tier)
   - Consider caching responses

## 🚀 ENHANCED COLLECTION STRATEGY

### Multi-Source Approach:
1. **Primary:** Use authenticated APIs
2. **Secondary:** Use public endpoints with proper parameters  
3. **Tertiary:** Use related data sources (GBIF for IUCN status)
4. **Quaternary:** Use static datasets when available

### Error Handling:
```python
def robust_api_call(url, params, headers=None):
    for attempt in range(3):  # Retry logic
        try:
            response = requests.get(url, params=params, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limited
                time.sleep(60)  # Wait and retry
                continue
            else:
                logger.warning(f"API returned {response.status_code}: {response.text[:100]}")
                break
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(5)
    return None
```

### Data Validation:
- Verify coordinates are within expected geographic bounds
- Check taxonomic hierarchy consistency
- Validate temporal data ranges
- Cross-reference with multiple sources when possible

## 📊 SUCCESS METRICS

With proper API access, you can expect:
- **eBird:** 1000+ bird observations per query
- **iNaturalist:** 1000+ species observations per query  
- **IUCN:** Complete conservation status for Madagascar species
- **GBIF:** Unlimited occurrence records
- **NASA FIRMS:** Real-time fire detection data

## 🔗 USEFUL RESOURCES

- **eBird API Documentation:** https://documenter.getpostman.com/view/664302/S1ENwy59
- **iNaturalist API Documentation:** https://www.inaturalist.org/pages/api+reference
- **IUCN Red List API Documentation:** https://apiv3.iucnredlist.org/api/v3/docs
- **GBIF API Documentation:** https://www.gbif.org/developer/summary
- **NASA FIRMS API Documentation:** https://firms.modaps.eosdis.nasa.gov/api/

Remember: Always respect API rate limits and terms of service!
