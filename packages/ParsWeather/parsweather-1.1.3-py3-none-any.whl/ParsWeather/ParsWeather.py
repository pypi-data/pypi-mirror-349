import requests
from bs4 import BeautifulSoup
import random
import time
from urllib.parse import urljoin
from geopy.geocoders import Nominatim


class WeatherForecast:
    
    def get_GEO(city):
        url = f"https://www.accuweather.com/web-api/autocomplete?query={city}&language=en-us"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
        
            if data and isinstance(data, list) and "key" in data[0]:
                city_key = data[0]["key"]
                return city_key
            else:
                return "Key not found in response!"
        else:
            return response.status_code
        
    def url_weather_forecast(key):
        
        url = f"https://www.accuweather.com/web-api/three-day-redirect?key={key}&postalCode="


        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }


        response = requests.get(url, allow_redirects=True, headers=headers)


        redirected_url = response.url


        translated_url = redirected_url.replace("/en/", "/fa/")

        return translated_url


    def url_air_quality_index(key):
        
        url = f"https://www.accuweather.com/web-api/three-day-redirect?key={key}&postalCode="


        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }


        response = requests.get(url, allow_redirects=True, headers=headers)


        redirected_url = response.url


        translated_url = redirected_url.replace("/en/", "/fa/")

        airqualityindex = translated_url.replace("/weather-forecast/","/air-quality-index/")

        return airqualityindex


    def url_health_activities(key):
        
        url = f"https://www.accuweather.com/web-api/three-day-redirect?key={key}&postalCode="


        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }


        response = requests.get(url, allow_redirects=True, headers=headers)


        redirected_url = response.url


        translated_url = redirected_url.replace("/en/", "/fa/")

        airqualityindex = translated_url.replace("/weather-forecast/","/health-activities/")

        return airqualityindex

    def url_daily_weather(key):
        
        url = f"https://www.accuweather.com/web-api/three-day-redirect?key={key}&postalCode="

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, allow_redirects=True, headers=headers)

        redirected_url = response.url

        translated_url = redirected_url.replace("/en/", "/fa/")

        airqualityindex = translated_url.replace("/weather-forecast/","/daily-weather-forecast/")

        return airqualityindex


    @classmethod
    def get_daily_weather_info(cls,city_name, target_date):
        """دریافت اطلاعات آب و هوایی یک شهر"""
        GEO = WeatherForecast.get_GEO(city_name)
        url = WeatherForecast.url_daily_weather(GEO)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return "خطا در دریافت اطلاعات از سایت"

        soup = BeautifulSoup(response.text, "html.parser")

        daily_cards = soup.find_all("div", class_="daily-wrapper")

        for card in daily_cards:
            date_element = card.find("span", class_="module-header sub date")
            if date_element and date_element.text.strip() == target_date:
                high_temp = card.find("span", class_="high").text.strip()
                low_temp = card.find("span", class_="low").text.strip()
                precip = card.find("div", class_="precip").text.strip()
                condition = card.find("div", class_="phrase").text.strip()

                wind_speed = "نامشخص"
                panel_items = card.find_all("p", class_="panel-item")

                for item in panel_items:
                    if "باد" in item.text:
                        wind_speed = item.text.replace("باد", "").strip()
                        break


                return {
                    "تاریخ": target_date,
                    "دمای بالا": high_temp,
                    "دمای پایین": low_temp,
                    "احتمال بارش": precip,
                    "وضعیت هوا": condition,
                    "سرعت باد": wind_speed
                }

        return "تاریخ موردنظر یافت نشد."


    @classmethod
    def get_temperature(cls, city_name):
        """دریافت دمای کنونی یک شهر"""
        GEO = WeatherForecast.get_GEO(city_name)
        url = WeatherForecast.url_weather_forecast(GEO)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            temp_tag = soup.find(class_='temp')
            return temp_tag.text.strip() if temp_tag else "دما یافت نشد."
        else:
            return f"خطا در دریافت صفحه: {response.status_code}"

    @classmethod
    def get_realfeel(cls, city_name):
        """دریافت دمای احساسی (RealFeel) یک شهر"""
        GEO = WeatherForecast.get_GEO(city_name)
        url = WeatherForecast.url_weather_forecast(GEO)
        


        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            return f"⚠️ خطا در دریافت صفحه: {e}"

        soup = BeautifulSoup(response.text, 'html.parser')

        realfeel_div = soup.find('div', class_='real-feel')
    
        if realfeel_div:
            realfeel_text = realfeel_div.get_text(strip=True)  
            realfeel_value = realfeel_text.replace("RealFeel®", "").strip()  
            return f"{realfeel_value}"
    
        return "⚠️ اطلاعات دمای احساسی یافت نشد."   


    @classmethod
    def get_wind(cls,city_name):
        '''دریافت سرعت باد یک شهر'''
        GEO = WeatherForecast.get_GEO(city_name)
        url = WeatherForecast.url_weather_forecast(GEO)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            wind_label = soup.find('span', class_='label', string='باد')
            if wind_label:
                value_tag = wind_label.find_next('span', class_='value')
                if value_tag:
                    return value_tag.text.strip()
                else:
                    return "نمیدونم"
            else:
                return "نمیدونم"
        else:
            return f"خطا در دریافت صفحه: {response.status_code}"
    
    @classmethod
    def get_air_quality(cls,city_name):
        '''دریافت کیفیت هوا یک شهر'''
        GEO = WeatherForecast.get_GEO(city_name)
        url = WeatherForecast.url_weather_forecast(GEO)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            air_quality_label = soup.find('span', class_='label', string='کیفیت هوا')
            if air_quality_label:
                value_tag = air_quality_label.find_next('span', class_='value')
                if value_tag:
                    return value_tag.text.strip()
                else:
                    return "مقدار کیفیت هوا پیدا نشد."
            else:
                return "برچسب 'کیفیت هوا' پیدا نشد."
        else:
            return f"خطا در دریافت صفحه: {response.status_code}"


    @classmethod
    def get_radar_image_link(cls,city_name):
        """دریافت لینک تصویر رادار یک شهر"""
        GEO = WeatherForecast.get_GEO(city_name)
        url = WeatherForecast.url_weather_forecast(GEO)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            radar_link_tag = soup.find("a", class_="base-map-cta card static-radar-map-recommended")
            if radar_link_tag:
                img_tag = radar_link_tag.find("img")
                if img_tag:
                    image_url = img_tag.get("data-src")
                    if image_url:
                        random_param = f"?t={int(time.time())}_{random.randint(1000, 9999)}"
                        return image_url + random_param 
                    else:
                        return "مقدار data-src یافت نشد."
                else:
                    return "تگ <img> یافت نشد."
            else:
                return "تگ <a> مورد نظر یافت نشد."
        else:
            return f"خطا در بارگذاری صفحه: {response.status_code}"

    @classmethod
    def get_sun_times(cls,city_name):
        '''دریافت زمان خروج و ورود خورشید و ماه یک شهر'''
        GEO = WeatherForecast.get_GEO(city_name)
        url = WeatherForecast.url_weather_forecast(GEO)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()   

            soup = BeautifulSoup(response.text, 'html.parser')

            items = soup.find_all('div', class_='sunrise-sunset__item')

            sun_times = {}

            for item in items:
                phrase = item.find('span', class_='sunrise-sunset__phrase').text.strip() 
            
                if "ساعت" in phrase:  
                    times = item.find('div', class_='sunrise-sunset__times')

                    if times:
                        time_items = times.find_all('div', class_='sunrise-sunset__times-item')
                        time_dict = {}

                        for time_item in time_items:
                            label = time_item.find('span', class_='sunrise-sunset__times-label').text.strip()
                            value = time_item.find('span', class_='sunrise-sunset__times-value').text.strip()
                            time_dict[label] = value

                        sun_times[phrase] = time_dict

            return sun_times

        except requests.exceptions.RequestException as e:
            return f"خطا در دریافت صفحه: {e}"

    @classmethod
    def get_weather_forecast(cls,city_name):
        '''دریافت اب هوا برای چند روز'''
        GEO = WeatherForecast.get_GEO(city_name)
        url = WeatherForecast.url_weather_forecast(GEO)
    
        headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0"
        }

        response = requests.get(url,headers=headers)
        response.raise_for_status() 

        soup = BeautifulSoup(response.text, 'html.parser')

        daily_list = soup.find('div', class_='daily-list content-module')

        daily_items = daily_list.find_all('a', class_='daily-list-item')

        forecast_data = []   

        for item in daily_items:
            date = item.find('div', class_='date').get_text(strip=True)
            temp_hi = item.find('span', class_='temp-hi').get_text(strip=True)
            temp_lo = item.find('span', class_='temp-lo').get_text(strip=True)
            icon_url = item.find('img', class_='icon')['src']
        
            forecast_data.append({
                "تاریخ": date,
                "دمای بالا": temp_hi,
                "دمای پایین": temp_lo,
                "آیکن وضعیت آب و هوا": icon_url
            })

        return forecast_data

    @classmethod
    def get_dust_dander_data(cls,city_name):
        '''دریافت اطلاعات گرد و غبار و درمان آن'''
        GEO = WeatherForecast.get_GEO(city_name)
        url = WeatherForecast.url_weather_forecast(GEO)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
        response = requests.get(url, headers=headers)
    
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            dust_dander_section = soup.find('a', {'data-slug': 'dust-dander'})
        
            if dust_dander_section:
                name = dust_dander_section.find('span', class_='health-activities__item__name').text.strip()
                category = dust_dander_section.find('span', class_='health-activities__item__category').text.strip()
                unsupported_category = dust_dander_section.find('span', class_='health-activities__item__category__unsupported').text.strip()

                return {
                    'name': name,
                    'category': category,
                    'unsupported_category': unsupported_category
                }
            else:
                return "داده‌ها پیدا نشدند"
        else:
            return f"خطا در بارگذاری صفحه: {response.status_code}"

    @classmethod
    def get_title(cls,city_name):
        '''دریافت عنوان شهر'''
        GEO = WeatherForecast.get_GEO(city_name)
        url = WeatherForecast.url_weather_forecast(GEO)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
        response = requests.get(url, headers=headers)
    
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
        
            title = soup.find("title")

            if title:
                return title.text
            else:
                return "نمیدونم"
        else:
            return f"خطا در دریافت صفحه: {response.status_code}"
  
    @classmethod    
    def get_forecast_details(cls,city_name):
        '''دریافت پیش بینی اب هوا'''
        GEO = WeatherForecast.get_GEO(city_name)
        url = WeatherForecast.url_weather_forecast(GEO)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            forecast_link = soup.find("a", class_="local-forecast-summary")
            
            if forecast_link:
                forecast_title = forecast_link.find("h2").text if forecast_link.find("h2") else "عنوان پیدا نشد"
                forecast_description = forecast_link.find("p").text if forecast_link.find("p") else "توضیح پیدا نشد"
                
                return forecast_title, forecast_description
            else:
                return "خبر ندارم", ""
        else:
            return "درخواست ناموفق بود", ""


    @classmethod
    def get_air_quality_aqi(cls,city_name):
        '''دریافت اطلاعات میزان شاخص الودگی هوا'''
        GEO = WeatherForecast.get_GEO(city_name)
        url = WeatherForecast.url_air_quality_index(GEO)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            air_quality_div = soup.find('div', class_='aq-number-wrapper')
            air_quality_details = soup.find('h3', class_='air-quality-data')

            if air_quality_div and air_quality_details:
                air_quality_value = air_quality_div.find('div', class_='aq-number').text.strip()
                unit = air_quality_div.find('div', class_='aq-unit').text.strip()

                category_text = air_quality_details.find('p', class_='category-text').text.strip()
                statement = air_quality_details.find('p', class_='statement').text.strip()

                return air_quality_value, unit, category_text, statement
            else:
                return None, None, "شاخص کیفیت هوا یافت نشد", "توضیحات یافت نشد"
        else:
            return None, None, f"خطا در دریافت داده‌ها: {response.status_code}", "توضیحات یافت نشد"

    @classmethod
    def get_weather_forecast_air_aqi(cls,city_name):
        '''دریافت اطلاعات الودگی برای چند روز'''
        GEO = WeatherForecast.get_GEO(city_name)
        url = WeatherForecast.url_air_quality_index(GEO)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        daily_forecast = soup.find_all('div', class_='air-quality-content')

        forecast_data = []

        for day in daily_forecast:
            day_of_week = day.find('p', class_='day-of-week').text.strip()
            date = day.find('p', class_='date').text.strip()
            aqi = day.find('div', class_='aq-number').text.strip()

            forecast_data.append({
                'day_of_week': day_of_week,
                'date': date,
                'aqi': aqi
            })

        return forecast_data    
    
    @classmethod    
    def get_health_activities(cls,city_name):
        GEO = WeatherForecast.get_GEO(city_name)
        url = WeatherForecast.url_health_activities(GEO)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
    
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            health_cards = soup.find_all('a', class_='index-list-card')

            if not health_cards:
                return "هیچ اطلاعاتی یافت نشد."

            results = []
            for card in health_cards:
                title_tag = card.find('div', class_='index-name')
                status_tag = card.find('div', class_='index-status-text')

                if title_tag and status_tag:
                    title = title_tag.text.strip()
                    status = status_tag.text.strip()
                    results.append(f"{title}: {status}")

            return results
    
        else:
            return f"خطا در دریافت صفحه: {response.status_code}"

    @classmethod
    def download_specific_image(cls,url = "https://www.havajanah.ir/"):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url,headers=headers)
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            img_tag = soup.find('img', alt="تصویر ماهواره ای متحرک")

            if img_tag and 'src' in img_tag.attrs:
                gif_url = img_tag['src']
                gif_url = urljoin(url, gif_url)    
                return gif_url
            else:
                return "تگ img یا لینک src یافت نشد."
            
        except requests.exceptions.RequestException as e:
            print(f"Erorr: {e}")

    @classmethod
    def get_pollutant_info(cls, city_name):
        '''دریافت اطلاعات گوگرد دی اکسید و گوگرد دی اکسید'''
        GEO = WeatherForecast.get_GEO(city_name)
        url = WeatherForecast.url_air_quality_index(GEO)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            pollutants = soup.find_all('div', class_='air-quality-pollutant')
            
            pollutant_info = {}
            
            for pollutant in pollutants:
                pollutant_name = pollutant.find('h3').text.strip()
                
                concentration = pollutant.find('div', class_='pollutant-concentration').text.strip()
                
                statement = pollutant.find('div', class_='statement').text.strip()
                
                pollutant_info[pollutant_name] = {
                    'concentration': concentration,
                    'statement': statement
                }
                
            return pollutant_info
        else:
            return f"خطا در درخواست: {response.status_code}"

    @classmethod
    def get_earth_satellite_image_url(cls):
        url = 'https://www.havajanah.ir/sat-pic/%d8%aa%d8%b5%d9%88%db%8c%d8%b1-%d8%a8%d8%a7%da%a9%db%8c%d9%81%db%8c%d8%aa-%d9%88-%d9%88%d8%a7%d9%82%d8%b9%db%8c-%da%a9%d8%b1%d9%87-%d8%b2%d9%85%db%8c%d9%86/'  
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            image_div = soup.find('div', class_='wp-caption aligncenter')

            if image_div:  
                image_tag = image_div.find('img')
                if image_tag:
                    return image_tag['src']
                else:
                    return "تصویر پیدا نشد"
            else:
                return "تگ div با کلاس 'wp-caption aligncenter' پیدا نشد"
        else:
            return f"خطا در درخواست: {response.status_code}"


class Location:

    @classmethod
    def get_coordinates(cls, city_name):
        try:
            geolocator = Nominatim(user_agent="ParsWeather")
            location = geolocator.geocode(city_name)
            if location:
                return {"lat": location.latitude, "lon": location.longitude}
            else:
                return "❌ City not found."
        except Exception as e:
            return f"💥 Error: {e}"
        
    @classmethod
    def get_location_name(cls, lat, lon, lang='en'):
        try:
            geolocator = Nominatim(user_agent="ParsWeather")
            location = geolocator.reverse((lat, lon), language=lang)
            if location:
                address = location.raw.get('address', {})
                city = address.get('city') or address.get('town') or address.get('village') or address.get('state_district')
                if city:
                    return city
                else:
                    return location.address
            else:
                return "❌ Location not found."
        except Exception as e:
            return f"💥 Error: {e}"

    @classmethod
    def get_full_address(cls, lat, lon, lang='en'):
        try:
            geolocator = Nominatim(user_agent="ParsWeather")
            location = geolocator.reverse((lat, lon), language=lang)
            if location:
                return location.address
            else:
                return "❌ Location not found."
        except Exception as e:
            return f"💥 Error: {e}"
