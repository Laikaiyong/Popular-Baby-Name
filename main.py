# A _connect() method to set up and return the underlying connection object
# A way to retrieve the underlying connection object (such as a cursor() method)
import streamlit as st
from streamlit.connections import ExperimentalBaseConnection
import supabase

class SupabaseConnection(ExperimentalBaseConnection[supabase]):
    def __init__(self):
        ...
    
    def _connect(self, **kwags):
        connector = st.experimental_connection(
            'babynames_db',
            type="sql"
        )
        
        return connector

    def cursor(self):
        return self._connect()

    @st.cache_data
    def query(
        _self, 
        originalDataframe,
        year_select,
        gender_select
    ):
        filter_baby_names = originalDataframe
        if year_select == "All" and gender_select == "All":
            filter_baby_names = originalDataframe
        elif year_select != "All" and gender_select == "All":
            filter_baby_names = originalDataframe[originalDataframe['Year']== year_select]
        elif year_select == "All" and gender_select != "All":
            filter_baby_names = originalDataframe[originalDataframe['Gender']== gender_select]
        else:
            filter_baby_names = originalDataframe[(originalDataframe['Gender']==gender_select) & (originalDataframe['Year']==year_select)]
        
        return filter_baby_names
        
    
conn = SupabaseConnection().cursor()

baby_names = conn.query('select * from baby_names')
baby_names['Year'].apply(str)
baby_names = baby_names.drop(['Id'], axis=1)

filter_baby_names = baby_names

baby_names_year = baby_names['Year'].unique().tolist()
baby_names_year.insert(0, "All")

year_selected = st.sidebar.selectbox('Pick year', baby_names_year)
gender_selected = st.sidebar.selectbox('Pick gender', ["All", "M", "F"])

filter_baby_names = SupabaseConnection().query(
    baby_names,
    year_selected,
    gender_selected
)
    
st.title('Popular Baby Name')
st.dataframe(filter_baby_names, hide_index=True)