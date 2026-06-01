import streamlit as st
import pandas as pd
#from streamlit_local_storage import LocalStorage

# 1. Basic Mobile UI Configuration
st.set_page_config(page_title="PoT Dino Stats", page_icon="🦖", layout="centered")

# Initialize the phone hardware local storage engine
#local_storage = LocalStorage()

st.title("🦖 PoT Dino Stats Reference")

# 2. LOAD DATA (Safe execution block)
@st.cache_data
def load_data():
    dinos = pd.read_csv("dinos.csv")
    abilities = pd.read_csv("abilities.csv")
    return dinos, abilities

# We run the data loading safely right here
try:
    df_dinos, df_abilities = load_data()
    data_loaded = True
except Exception as e:
    st.error("Missing file error: Please ensure 'dinos.csv' and 'abilities.csv' are uploaded to your repository.")
    data_loaded = False

# 3. RUN INTERFACE ONLY IF DATA LOADED SUCCESSFULLY
if data_loaded:
    dino_names = df_dinos['Name'].tolist()
    
    # Fetch save coordinates
   # saved_log = local_storage.getItem("pot_logout_locations")
   # if saved_log is None:
    #    saved_log = {name: "" for name in dino_names}
  #  else:
        # Ensures new dinos get their own blank row later
     #   for name in dino_names:
       #     if name not in saved_log:
        #        saved_log[name] = ""

    # Logout Tracker
 #   with st.expander("📝 Show Logout Location Tracker"):
     #   st.markdown("*Type your logout location.*")

     #   log_data = pd.DataFrame({
       #     "Dinosaur": dino_names,
        #    "Last Logged Location": [saved_log.get(name, "") for name in dino_names]
     #   })

      #  edited_df = st.data_editor(
        #    log_data,
        #    column_config={
         #       "Dinosaur": st.column_config.TextColumn(disabled=True),
         #       "Last Logged Location": st.column_config.TextColumn(width="large")
         #   },
         #   disabled=False,
         #   num_rows="fixed",
          #  hide_index=True,
          #  use_container_width=True
       # )

        # Check for new content
     #   updated_log = {}
     #   has_changes = False
      #  for idx, row in edited_df.iterrows():
      #      dino_name = row['Dinosaur']
       #     new_loc = str(row['Last Logged Location']).strip()
       #     updated_log[dino_name] = new_loc
       #     if saved_log.get(dino_name) != new_loc:
       #         has_changes = True

      #  if has_changes:
      #      local_storage.setItem("pot_logout_locations", updated_log)
       #     st.rerun()

 #   st.markdown("---")
    
    # --- SEARCH & SELECTION INTERFACE ---
    search_query = st.text_input("🔍 Search Dinosaurs...", "").strip()

    if search_query:
        filtered_dinos = df_dinos[df_dinos['Name'].str.contains(search_query, case=False, na=False)]
    else:
        filtered_dinos = df_dinos

    dino_list = filtered_dinos['Name'].tolist()

    if dino_list:
        selected_dino = st.selectbox("Select a Dinosaur to view stats:", dino_list)
        dino_row = df_dinos[df_dinos['Name'] == selected_dino].iloc[0]

        # --- PROFILE HEADER & IMAGE ---
        st.markdown(f"### 🛡️ {selected_dino} Profile")

        dino_image = dino_row['Main Dino Image']
        if pd.notna(dino_image) and str(dino_image).strip() != "":
            st.image(str(dino_image).strip(), use_container_width=True)

        st.markdown("---")

        # --- CORE NUMERIC METRICS ---
        col1, col2 = st.columns(2)
        with col1:
            st.metric("❤️ Max Health", f"{int(dino_row['Health'])}")
            st.metric("🛡️ Armor", f"{dino_row['Armor']}")
            st.metric("🏃 Sprint Time", f"{dino_row['Sprint Time']}s")
        with col2:
            st.metric("⚖️ Combat Weight", f"{int(dino_row['Combat Weight'])}")
            st.metric("👥 Group Size", f"{int(dino_row['Group Size'])}")

        # --- STAR ATTRIBUTE RATINGS ---
        st.markdown("---")
        st.markdown("### 📊 Attribute Ratings")

        def get_stars(val):
            val_str = str(val).strip()
            if pd.isna(val) or val_str in ["", "nan", "None"]:
                return "—"
            return val_str

        st.write(f"**⚔️ Damage:** {get_stars(dino_row['Damage'])}")
        st.write(f"**🛡️ Defense:** {get_stars(dino_row['Defense'])}")
        st.write(f"**🔄 Recovery:** {get_stars(dino_row['Recovery'])}")
        st.write(f"**🪵 Land Speed:** {get_stars(dino_row['Land Speed'])}")
        st.write(f"**🌊 Water Speed:** {get_stars(dino_row['Water Speed'])}")
        st.write(f"**☠️ Survivability:** {get_stars(dino_row['Survivability'])}")

        st.markdown("---")
        st.markdown(f"**Clampable By:** {dino_row['Clampable By']}")
        st.markdown(f"**Subspecies Bonuses:**\n{dino_row['Subspecies']}")

        # --- External Interactive Map URL LINK ---
        st.markdown("---")
        st.link_button("Click to see interactive map on potservers.net", "https://potservers.net/map", use_container_width=True)

        # --- RELATIONAL COMBAT ABILITIES ---
        st.markdown("---")
        st.markdown("### ⚔️ Combat Abilities")

        current_dino_id = dino_row['Dino ID']
        matching_abilities = df_abilities[df_abilities['Dino ID'] == current_dino_id]

        if not matching_abilities.empty:
            for _, row in matching_abilities.iterrows():
                with st.expander(f"{str(row['Slot']).upper()}: {row['Ability Name']}"):
                    st.write(f"**Damage:** {row['Damage']} | **Cooldown:** {row['Cooldown']}s")
                    st.info(row['Description'])
        else:
            st.warning("No combat abilities documented for this dinosaur yet.")
