import pandas as pd
import streamlit as st
import altair as alt


@st.cache_data
def load_data(csv_path):
    return pd.read_csv(csv_path)

# Load the data
# college_name_csv = load_data('./college_name_list.csv')
df = load_data('./college_df.csv')
df.rename({'Unnamed: 0':'Name'}, axis = 1, inplace = True)

# title
st.markdown("# comparing college cost.")

col1, col2 = st.columns(2)

with col1:
    col1_college_name = st.selectbox("Select a college", df['Name'], key=1)
    col1_college_data = df[df['Name'] == col1_college_name]

    st.write(f"Data for {col1_college_name}:")
    st.dataframe(col1_college_data.transpose(), width=300, height=300)

with col2:
    col2_college_name = st.selectbox("Select a college", df['Name'], key=2)
    col2_college_data = df[df['Name'] == col2_college_name]

    st.write(f"Data for {col2_college_name}:")
    st.dataframe(col2_college_data.transpose(), width=300, height=300)

selected_colleges = df[df['Name'].isin([col1_college_name, col2_college_name])]
cost_data = selected_colleges.melt(id_vars=['Name'], 
                                   value_vars=['Outstate', 'Room.Board', 'Books'],
                                   var_name='Cost Type',
                                   value_name='Amount')

chart = alt.Chart(cost_data).mark_bar().encode(
    x='Name:O',
    y='sum(Amount):Q',
    color='Cost Type:N',
    tooltip=['Name', 'Cost Type', 'Amount']).properties(
        title='Comparison of Tuition Costs Between Two Colleges'
    )

st.altair_chart(chart, use_container_width=True)