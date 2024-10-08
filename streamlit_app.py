# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Cutomize your Smoothie :cup_with_straw: ")
st.write(
    """Choose the fruits you want in your smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on Smoothie will be", name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
 )

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    ingredients_string = ''
    for x in ingredients_list:
        ingredients_string +=x + ' '

    st.write(ingredients_string)
    
    my_insert_stmt = """INSERT INTO smoothies.public.orders (name_on_order, ingredients) 
            values ('""" + name_on_order + """','""" + ingredients_string + """')"""

    st.write(my_insert_stmt)
    
    if ingredients_string:
       session.sql(my_insert_stmt).collect()
       st.success('Your Smoothie is ordered!', icon="✅")

