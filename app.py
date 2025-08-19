import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from vedicastro.VedicAstro import VedicHoroscopeData
from timezonefinder import TimezoneFinder
import pytz
from geopy.geocoders import Nominatim
import swisseph as swe
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
import os
import urllib.request
import zipfile
from pathlib import Path
import flatlib
import shutil
import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

AYAN = "Lahiri"
HOUSE_SYSTEM = "Placidus"

dst = Path.home() / "ephe"
dst.mkdir(parents=True, exist_ok=True)
src = Path(flatlib.__file__).parent / "resources" / "swefiles"
if src.exists() and src.is_dir():
    try:
        shutil.copytree(src, dst, dirs_exist_ok=True)
    except Exception as e:
        pass

EPHE_URL_BASE = "https://www.astro.com/ftp/swisseph/ephe/"
ESSENTIAL_FILES = ["seas_18.se1","semo_18.se1","sepl_18.se1"]

def setup_swiss_ephemeris_auto(ephe_subdir="ephe", app_root=None, verbose=True):
    try:
        base = app_root or os.getcwd()
        ephe_path = os.path.join(base, ephe_subdir)
        os.makedirs(ephe_path, exist_ok=True)
        swe.set_ephe_path(ephe_path)
        for fname in ESSENTIAL_FILES:
            target = os.path.join(ephe_path, fname)
            if not (os.path.exists(target) and os.path.getsize(target) > 2000):
                url = EPHE_URL_BASE + fname
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=60) as resp, open(target, 'wb') as out_f:
                        shutil.copyfileobj(resp, out_f)
                except:
                    continue
        jd = swe.julday(2000, 1, 1, 12.0)
        try:
            swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH)
            return ephe_path
        except:
            try:
                swe.calc_ut(jd, swe.SUN, swe.FLG_MOSEPH)
                return "moshier"
            except:
                return None
    except:
        return None

def get_location_coordinates(place_name):
    try:
        geolocator = Nominatim(user_agent="astro_app")
        location = geolocator.geocode(place_name)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except:
        return None, None

def calculate_utc_offset(latitude, longitude, year, month, day, hour, minute, second):
    try:
        tf = TimezoneFinder()
        tz_str = tf.timezone_at(lat=latitude, lng=longitude)
        if tz_str:
            tz = pytz.timezone(tz_str)
            dt = datetime(year, month, day, hour, minute, second)
            utc_offset = tz.utcoffset(dt)
            return int(utc_offset.total_seconds() / 3600)
        else:
            return 0
    except:
        return 0

def parse_date_time(date_string, time_string):
    try:
        date_obj = datetime.strptime(date_string, "%d/%m/%Y")
        time_obj = datetime.strptime(time_string, "%H:%M:%S")
        return (date_obj.year, date_obj.month, date_obj.day,time_obj.hour, time_obj.minute, time_obj.second)
    except:
        return None

def normalize_retrograde_flag(is_retro):
    return -1 if is_retro else 0

def convert_to_tropical(sidereal_longitude, ayanamsa):
    return (sidereal_longitude + ayanamsa) % 360

def create_chart_parameters(planet_dict, houses_data, year, month, day, hour, minute, second, utc_offset):
    try:
        ut_hour = hour - utc_offset + minute / 60 + second / 3600
        jd = swe.julday(year, month, day, ut_hour)
        try:
            swe.set_sid_mode(swe.SIDM_LAHIRI)
            ayanamsa = swe.get_ayanamsa(jd)
        except:
            ayanamsa = 23.85
        params = {"Width": 850,"Height": 1100,"ChartStyle": 2,"birthTimeZone": utc_offset,"birthDST": 0,"birthJulDay": jd}
        planets = ["Asc","Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"]
        planet_codes = ["Lg","Su","Mo","Ma","Me","Ju","Ve","Sa","Ra","Ke"]
        for planet, code in zip(planets, planet_codes):
            if planet in planet_dict:
                sidereal_lon = planet_dict[planet]["LonDecDeg"]
                tropical_lon = convert_to_tropical(sidereal_lon, ayanamsa)
                params[f"{code}_Full_Degrees"] = tropical_lon
                params[f"{code}_Full_Degree_Sidereal"] = sidereal_lon
        retro_planets = {"Mars": "Ma","Mercury": "Me","Jupiter": "Ju","Venus": "Ve","Saturn": "Sa"}
        for planet, code in retro_planets.items():
            if planet in planet_dict:
                params[f"{code}_Retro"] = normalize_retrograde_flag(planet_dict[planet]["isRetroGrade"])
        for house in houses_data:
            house_tropical = convert_to_tropical(house.LonDecDeg, ayanamsa)
            params[f"HouseCusp{house.HouseNr}"] = house_tropical
        return params
    except:
        return None

def get_chart_image(params):
    try:
        base_url = "https://vaultoftheheavens.com/VOTH_ChartCreator/BasicPrintout.aspx"
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return None

def extract_planet_data(planets_data):
    planet_dict = {}
    for data in planets_data:
        planet_name = getattr(data, "Object", None)
        if planet_name:
            planet_dict[planet_name] = {
                "Rasi": getattr(data, "Rasi", None),
                "isRetroGrade": getattr(data, "isRetroGrade", None),
                "LonDecDeg": getattr(data, "LonDecDeg", None),
                "SignLonDMS": getattr(data, "SignLonDMS", None),
                "SignLonDecDeg": getattr(data, "SignLonDecDeg", None),
                "LatDMS": getattr(data, "LatDMS", None),
                "Nakshatra": getattr(data, "Nakshatra", None),
                "RasiLord": getattr(data, "RasiLord", None),
                "NakshatraLord": getattr(data, "NakshatraLord", None),
                "SubLord": getattr(data, "SubLord", None),
                "SubSubLord": getattr(data, "SubSubLord", None),
                "HouseNr": getattr(data, "HouseNr", None),
            }
    return planet_dict

def extract_significator_data(significator_table):
    significator_dict = {}
    for data in significator_table:
        key = getattr(data, "House", None) or getattr(data, "Planet", None)
        if key:
            significator_dict[key] = {"A": getattr(data, "A", None),"B": getattr(data, "B", None),"C": getattr(data, "C", None),"D": getattr(data, "D", None)}
    return significator_dict

def generate_astrology_reading(planet_data, house_significators, planet_significators, vimshottari_dasa, user_name, user_question=None):
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",api_key=gemini_api_key)
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        system_prompt = f"""You are an expert Vedic astrologer. Provide readings for {user_name}.
        Data:
        - Planet Data: {planet_data}
        - House Significators: {house_significators}
        - Planet Significators: {planet_significators}
        - Vimshottari Dasa: {vimshottari_dasa}"""
        if not user_question:
            user_input = f"Please provide a complete Vedic astrology reading for {user_name}"
        else:
            user_input = user_question
        messages = [("system", system_prompt)]
        messages += st.session_state.chat_history
        messages.append(("user", user_input))
        response = llm.invoke(messages)
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("assistant", response.content))
        return response.content
    except:
        return None

def main():
    st.title("🌟 Vedic Astrology Reading with Chat")
    st.write("Get your personalized Vedic astrology reading and ask follow-up questions")
    try:
        setup_swiss_ephemeris_auto()
    except:
        return
    if "horoscope_data" not in st.session_state:
        st.session_state.horoscope_data = None
    if "chart_ready" not in st.session_state:
        st.session_state.chart_ready = False
    with st.form("astrology_form"):
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        with col1:
            date_input = st.text_input("Date of Birth (DD/MM/YYYY)", placeholder="09/01/2000")
        with col2:
            time_input = st.text_input("Time of Birth (HH:MM:SS)", placeholder="14:30:00")
        with col3:
            place_name = st.text_input("Place of Birth", placeholder="New York, NY")
        with col4:
            user_name = st.text_input("Your Name", placeholder="John Doe")
        submitted = st.form_submit_button("Generate Reading")
    if submitted:
        if not all([date_input, time_input, place_name, user_name]):
            st.error("Please fill in all fields")
            return
        parsed_datetime = parse_date_time(date_input, time_input)
        if not parsed_datetime:
            return
        year, month, day, hour, minute, second = parsed_datetime
        latitude, longitude = get_location_coordinates(place_name)
        if latitude is None:
            return
        utc_offset = calculate_utc_offset(latitude, longitude, year, month, day, hour, minute, second)
        try:
            vhd = VedicHoroscopeData(year=year, month=month, day=day,hour=hour, minute=minute, second=second,utc=utc_offset, latitude=latitude, longitude=longitude,ayanamsa=AYAN, house_system=HOUSE_SYSTEM)
            chart = vhd.generate_chart()
            planets_data = vhd.get_planets_data_from_chart(chart)
            houses_data = vhd.get_houses_data_from_chart(chart)
            vimshottari_dasa = vhd.compute_vimshottari_dasa(chart)
            planets_significators = vhd.get_planet_wise_significators(planets_data, houses_data)
            house_significators = vhd.get_house_wise_significators(planets_data, houses_data)
            planet_dict = extract_planet_data(planets_data)
            house_sig_dict = extract_significator_data(house_significators)
            planet_sig_dict = extract_significator_data(planets_significators)
            st.session_state.horoscope_data = {'planet_dict': planet_dict,'houses_data': houses_data,'house_significators': house_sig_dict,'planet_significators': planet_sig_dict,'vimshottari_dasa': vimshottari_dasa,'birth_data': (year, month, day, hour, minute, second, utc_offset),'user_name': user_name}
            st.session_state.chart_ready = True
            st.session_state.chat_history = []
            st.success(f"✅ Horoscope calculated successfully for {user_name}!")
        except:
            return
    if st.session_state.chart_ready and st.session_state.horoscope_data:
        data = st.session_state.horoscope_data
        if st.button("🔮 Get Detailed Reading"):
            reading = generate_astrology_reading(data['planet_dict'],data['house_significators'],data['planet_significators'],data['vimshottari_dasa'],data['user_name'])
            if reading:
                st.subheader(f"🌟 Astrology Reading for {data['user_name']}")
                st.write(reading)
        user_question = st.text_input("Ask a follow-up question")
        if st.button("Ask"):
            if user_question.strip():
                answer = generate_astrology_reading(data['planet_dict'],data['house_significators'],data['planet_significators'],data['vimshottari_dasa'],data['user_name'],user_question)
                if answer:
                    st.subheader("🔮 Answer")
                    st.write(answer)
        if st.button("🎨 Generate Chart Image"):
            year, month, day, hour, minute, second, utc_offset = data['birth_data']
            params = create_chart_parameters(data['planet_dict'],data['houses_data'],year, month, day, hour, minute, second, utc_offset)
            if params:
                chart_image = get_chart_image(params)
                if chart_image:
                    st.subheader("📊 Your Vedic Chart")
                    st.image(chart_image, caption="Your Vedic Astrology Chart", use_column_width=True)
                    buf = BytesIO()
                    chart_image.save(buf, format="PNG")
                    st.download_button(label="💾 Download Chart",data=buf.getvalue(),file_name=f"{data['user_name']}_vedic_chart.png",mime="image/png")

if __name__ == "__main__":
    main()
