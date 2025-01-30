# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session

from snowflake.snowpark.functions import col

name = st.text_input('Name on order')
st.write('Name on order is ', name)

# Write directly to the app
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose fruits you want
    """
)

cnx = st.connection("snowflake")
session = cnx.session()

#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))



st.dataframe(data=my_dataframe, use_container_width = True)


ing_list = st.multiselect('choose 5', my_dataframe, max_selections = 6)
if ing_list:

    ing_str = ''

    for f in ing_list:
        ing_str += f + ' '

 

    my_insert_stmt = """ insert into smoothies.public.orders(name_on_order, ingredients)
            values ('""" + name + """' ,'""" + ing_str + """')"""

    st.write(my_insert_stmt)


    time_to_insert = st.button('Submit')

    if time_to_insert and ing_str:

        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name + '!', icon="✅")
