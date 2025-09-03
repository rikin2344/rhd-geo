#!/usr/bin/env python3
"""
SKF Bearing API Scraper
Uses SKF's internal API to extract complete bearing specifications including dimensional data
Much cleaner and more reliable than HTML scraping
"""

import requests
import json
import time
from urllib.parse import urlencode

class SKFAPIBearingScraper:
    def __init__(self):
        self.api_base = "https://search.skf.com/prod/search-skfcom/rest/apps/commercial_catalogue_v1/searchers/details"
        self.session = requests.Session()
        
        # Set up headers to mimic browser request
        self.session.headers.update({
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://www.skf.com',
            'Referer': 'https://www.skf.com/au/products/rolling-bearings/ball-bearings/deep-groove-ball-bearings/',
            'Sec-Ch-Ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
        })
    
    def get_bearing_data(self, designation, system='metric'):
        """Fetch bearing data from SKF API"""
        # For 16000 series, don't add -2RS1 suffix
        if designation.startswith('16'):
            designation_to_use = designation
        else:
            # For other series, try with -2RS1 suffix first
            designation_to_use = f"{designation}-2RS1"
        
        params = {
            'designation': designation_to_use,
            'language': 'en',
            'system': system,  # 'metric' or 'imperial'
            'searcher': 'details',
            'site': '319'  # SKF Australia site
        }
        
        try:
            print(f"🔍 Fetching data for {designation_to_use} ({system})...")
            
            # Update referer for this specific bearing
            self.session.headers['Referer'] = f'https://www.skf.com/in/products/rolling-bearings/ball-bearings/deep-groove-ball-bearings/productid-{designation_to_use}'
            
            response = self.session.get(self.api_base, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data and 'documentList' in data and 'documents' in data['documentList'] and len(data['documentList']['documents']) > 0:
                print(f"✅ Successfully fetched data for {designation_to_use}")
                return data['documentList']['documents'][0]  # First document should be exact match
            else:
                print(f"❌ No data found for {designation_to_use}")
                return None
                
        except requests.RequestException as e:
            print(f"❌ API request failed for {designation}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON response for {designation}: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error for {designation}: {e}")
            return None
    
    def get_bearing_data_without_suffix(self, designation, system='metric'):
        """Fetch bearing data from SKF API without -2RS1 suffix"""
        params = {
            'designation': designation,
            'language': 'en',
            'system': system,  # 'metric' or 'imperial'
            'searcher': 'details',
            'site': '319'  # SKF Australia site
        }
        
        try:
            print(f"🔍 Fetching data for {designation} ({system}) without suffix...")
            
            # Update referer for this specific bearing without suffix
            self.session.headers['Referer'] = f'https://www.skf.com/in/products/rolling-bearings/ball-bearings/deep-groove-ball-bearings/productid-{designation}'
            
            response = self.session.get(self.api_base, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data and 'documentList' in data and 'documents' in data['documentList'] and len(data['documentList']['documents']) > 0:
                print(f"✅ Successfully fetched data for {designation}")
                return data['documentList']['documents'][0]  # First document should be exact match
            else:
                print(f"❌ No data found for {designation}")
                return None
                
        except requests.RequestException as e:
            print(f"❌ API request failed for {designation}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON response for {designation}: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error for {designation}: {e}")
            return None
    
    def extract_dimensions(self, bearing_data):
        """Extract dimensional data from the API response"""
        dimensions = {}
        
        try:
            # Process technical_specification section which contains the dimensional data
            if 'technical_specification' in bearing_data:
                for spec_section in bearing_data['technical_specification']:
                    if spec_section.get('category') == 'Dimensions':
                        for table in spec_section.get('tables', []):
                            for feature in table.get('features', []):
                                description = feature.get('description', '')
                                name = feature.get('name', '')
                                real_value = feature.get('real_value')
                                
                                # Map API fields to our standard dimension names
                                if description == 'd':
                                    dimensions['d'] = real_value
                                    print(f"✅ Found d (bore): {real_value} mm")
                                elif description == 'D':
                                    dimensions['D'] = real_value
                                    print(f"✅ Found D (outside): {real_value} mm")
                                elif description == 'B':
                                    dimensions['B'] = real_value
                                    print(f"✅ Found B (width): {real_value} mm")
                                elif description == 'd<sub>1</sub>' or 'Shoulder diameter' in name:
                                    dimensions['d1'] = real_value
                                    print(f"✅ Found d1 (shoulder): {real_value} mm")
                                elif description == 'D<sub>2</sub>' or 'Recess diameter' in name:
                                    dimensions['D2'] = real_value
                                    print(f"✅ Found D2 (recess): {real_value} mm")
                                elif description == 'r<sub>1,2</sub>' or 'Chamfer dimension' in name:
                                    dimensions['r1'] = real_value
                                    dimensions['r2'] = real_value  # r1 and r2 are the same
                                    print(f"✅ Found r1,r2 (chamfer): {real_value} mm")
            
            # Also extract from technical_data section for basic dimensions
            if 'technical_data' in bearing_data:
                for data_section in bearing_data['technical_data']:
                    if data_section.get('name') == 'Dimensions':
                        for row in data_section.get('rows', []):
                            name = row.get('name', '')
                            value = row.get('value')
                            
                            if 'Bore diameter' in name and 'd' not in dimensions:
                                dimensions['d'] = value
                                print(f"✅ Found d (bore) from tech_data: {value} mm")
                            elif 'Outside diameter' in name and 'D' not in dimensions:
                                dimensions['D'] = value
                                print(f"✅ Found D (outside) from tech_data: {value} mm")
                            elif 'Width' in name and 'B' not in dimensions:
                                dimensions['B'] = value
                                print(f"✅ Found B (width) from tech_data: {value} mm")
                
        except Exception as e:
            print(f"❌ Error extracting dimensions: {e}")
        
        return dimensions
    
    def get_complete_bearing_info(self, designation):
        """Get complete bearing information including dimensions"""
        print(f"\n🎯 Processing bearing: {designation}")
        print("=" * 50)
        
        # For 16000 series, try without suffix first
        if designation.startswith('16'):
            print("🔍 Trying 16000 series without suffix...")
            bearing_data = self.get_bearing_data_without_suffix(designation, 'metric')
            if not bearing_data:
                print("🔄 Trying imperial system...")
                bearing_data = self.get_bearing_data_without_suffix(designation, 'imperial')
        else:
            # For other series, try with -2RS1 suffix first
            bearing_data = self.get_bearing_data(designation, 'metric')
            if not bearing_data:
                print("🔄 Trying imperial system...")
                bearing_data = self.get_bearing_data(designation, 'imperial')
            
            # If still no data, try without suffix
            if not bearing_data:
                print("🔄 Trying without -2RS1 suffix...")
                bearing_data = self.get_bearing_data_without_suffix(designation, 'metric')
                if not bearing_data:
                    print("🔄 Trying without suffix (imperial)...")
                    bearing_data = self.get_bearing_data_without_suffix(designation, 'imperial')
        
        if not bearing_data:
            return None
        
        # Extract basic info
        result = {
            'model': designation,
            'api_url': f"{self.api_base}?{urlencode({'designation': designation, 'language': 'en', 'system': 'metric', 'searcher': 'details', 'site': '319'})}",
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Extract dimensions
        dimensions = self.extract_dimensions(bearing_data)
        if dimensions:
            result['dimensions'] = dimensions
            
        # Extract other useful data from API
        useful_fields = ['designation', 'description', 'weight', 'loadRatings', 'speedLimits']
        for field in useful_fields:
            if field in bearing_data:
                result[field] = bearing_data[field]
        
        # Save raw API response for debugging
        result['raw_api_data'] = bearing_data
        
        return result
    
    def scrape_multiple_bearings(self, model_list):
        """Scrape multiple bearings with rate limiting"""
        results = []
        
        for i, model in enumerate(model_list):
            result = self.get_complete_bearing_info(model)
            if result:
                results.append(result)
            
            # Rate limiting - be respectful to SKF's API
            if i < len(model_list) - 1:
                print("⏳ Waiting 2 seconds...")
                time.sleep(2)
        
        return results
    
    def save_results(self, results, filename='skf_api_data.json'):
        """Save results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Saved {len(results)} results to {filename}")
    
    def save_dimensions_only(self, results, filename='skf_dimensions_only.json'):
        """Save only the dimensional data in a clean format"""
        clean_data = {}
        
        for result in results:
            if 'dimensions' in result:
                clean_data[result['model']] = result['dimensions']
        
        with open(filename, 'w') as f:
            json.dump(clean_data, f, indent=2)
        
        print(f"💾 Saved clean dimensional data for {len(clean_data)} bearings to {filename}")

def main():
    """Main execution"""
    print("🚀 SKF Bearing API Scraper - 6800 Series")
    print("=" * 60)
    print("Using SKF's internal API to extract bearing specifications")
    print("Using alternate model numbers (61800-61820) for 6800 series")
    print("=" * 60)
    
    scraper = SKFAPIBearingScraper()
    
    # 6800 series models with their alternate model numbers
    # 6800 -> 61800, 6801 -> 61801, etc.
    model_mapping = {}
    for i in range(21):  # 6800 to 6820
        if i < 10:
            original_model = f"680{i}"
        else:
            original_model = f"68{i}"
        
        alternate_model = str(int(original_model) + 55000)
        model_mapping[alternate_model] = original_model
    
    # Use alternate model numbers for API calls
    alternate_models = list(model_mapping.keys())
    alternate_models.sort()  # Sort numerically
    
    print(f"📋 Processing {len(alternate_models)} models:")
    for alt, orig in model_mapping.items():
        print(f"  {alt} -> {orig}")
    
    results = scraper.scrape_multiple_bearings(alternate_models)
    
    if results:
        # Update model numbers in results to use original model numbers
        for result in results:
            alt_model = result['model']
            if alt_model in model_mapping:
                result['original_model'] = model_mapping[alt_model]
                result['alternate_model'] = alt_model
                result['model'] = model_mapping[alt_model]  # Use original model as primary
        
        scraper.save_results(results, 'skf_6800_series_data.json')
        scraper.save_dimensions_only(results, 'skf_6800_series_dimensions.json')
        
        print("\n📊 SUMMARY:")
        print("=" * 30)
        for result in results:
            model = result['model']
            alt_model = result.get('alternate_model', 'N/A')
            dims = result.get('dimensions', {})
            print(f"{model} (alt: {alt_model}): {len(dims)} dimensions - {list(dims.keys())}")
            
        print("\n🎯 Missing Dimensional Data Summary:")
        print("=" * 40)
        target_dims = ['d1', 'D2', 'r1', 'r2']
        for result in results:
            model = result['model']
            dims = result.get('dimensions', {})
            missing = [dim for dim in target_dims if dim not in dims]
            if missing:
                print(f"{model}: Missing {missing}")
            else:
                print(f"{model}: ✅ All target dimensions found")
    else:
        print("❌ No data extracted")

if __name__ == "__main__":
    main()
