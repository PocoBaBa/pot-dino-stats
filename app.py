import streamlit as st
import pandas as pd

# Basic Mobile UI Configuration
st.set_page_config(page_title="PoT Dino Stats", page_icon="🦖", layout="centered")

st.title("🦖 PoT Dino Stats Reference")

# 1. Load your exported CSV files
@st.cache_data
def load_data():
    dinos = pd.read_csv("dinos.csv")
    abilities = pd.read_csv("abilities.csv")
    return dinos, abilities

try:
    df_dinos, df_abilities = load_data()

    # 2. Main Search Bar Interface
    search_query = st.text_input("🔍 Search Dinosaurs...", "").strip()

    # Filter dataset based on search input
    if search_query:
        filtered_dinos = df_dinos[df_dinos['Name'].str.contains(search_query, case=False, 
na=False)]
    else:
        filtered_dinos = df_dinos

    # 3. List of Dinosaurs Selection Box
    dino_list = filtered_dinos['Name'].tolist()

    if dino_list:
        selected_dino = st.selectbox("Select a Dinosaur to view stats:", dino_list)

        # Pull matching dinosaur entry row data
        dino_row = df_dinos[df_dinos['Name'] == selected_dino].iloc[0]

        # Display Core Stats
        st.markdown(f"### 🛡️ {selected_dino} Profile")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Combat Weight", f"{int(dino_row['Combat Weight'])}")
            st.metric("Armor", f"{dino_row['Armor']}")
        with col2:
            st.metric("Sprint Time", f"{dino_row['Sprint Time']}s")
            st.metric("Group Size", f"{int(dino_row['Group Size'])}")

        st.markdown(f"**Clampable By:** {dino_row['Clampable By']}")
        st.markdown(f"**Subspecies Bonuses:** {dino_row['Subspecies']}")

        #Build link URL
        st.markdown("---")
        build_url = dino_row['Build URL']
        if pd.notna(build_url) and str(build_url).strip() != "":
            st.link_button(f"View {selected_dino} Build on DinoMeta.gg", build_url, use_container_width=True

        # 4. Filtered Abilities Section (The Sub-Page Heist Solution!)
        st.markdown("---")
        st.markdown("### ⚔️ Combat Abilities")

        # Match current Dino ID with Abilities Table Rows
        current_dino_id = dino_row['Dino ID']
        matching_abilities = df_abilities[df_abilities['Dino ID'] == current_dino_id]

        if not matching_abilities.empty:
            for _, row in matching_abilities.iterrows():
                with st.expander(f"{row['Slot'].upper()}: {row['Ability Name']}"):
                    st.write(f"**Damage:** {row['Damage']} | **Cooldown:** {row['Cooldown']}")
                    st.info(row['Description'])
        else:
            st.warning("No combat abilities documented for this dinosaur yet.")

except Exception as e:
    st.error("Please ensure 'dinos.csv' and 'abilities.csv' are uploaded alongside this script.")
