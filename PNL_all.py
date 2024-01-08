import streamlit as st
import datetime
import time

import pandas as pd

def login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Simulate a simple login check (replace this with actual authentication logic)
        if username == "VIKABH" and password == "VKB@321":
            st.success("Login successful!")
            return True
        else:
            st.error("Invalid credentials. Please try again.")
            return False

def fetch_data():
    try:
        df = pd.read_csv('M:\\append_testing\DC\PNL_Team.csv')
        df[['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL']] = df[['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL']].round(2)
        return df
    except Exception as e:
        print(f'Error fetching the data: {str(e)}')
        return None

def style_dataframe(df):
    return df.style.applymap(
        lambda x: 'color: green' if x > 0 else ('color: red' if x < 0 else 'color: black'),
        subset=['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL', 'PL_D10U5',
       'PL_U5U3', 'PinPout', 'Actual', 'ExpOptVal', 'With_Exch']
    )

def main():

    st.set_page_config(layout='wide')
    st.title("Login")

    # Display login form
    if login():
        # Display the content for logged-in users
        st.write("Welcome to the app! You are now logged in.")

        st.title('PNL Dashboard')

        # Create placeholders for dynamic content
        time_display = st.empty()
        total_dataframe_placeholder = st.empty()
        pnl_dataframe_placeholder = st.empty()

        while True:
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Read quantity_fetch_time.csv
            quantity_fetch_time_df = pd.read_csv('J:\\OutPut\\testing\\quantity_fetch_time.csv')
            quantity_fetch_time = pd.to_datetime(quantity_fetch_time_df['Fetch Time'].iloc[0])

            # Update time_display placeholder
            time_display.write(f'Current Time {current_time}   |   PNL Time {quantity_fetch_time}', format='md')

            # Fetch data
            pnl_df = fetch_data()

            if pnl_df is not None:
                # Calculate and append totals row
                totals_row = pnl_df.select_dtypes(include=['number']).sum()
                totals_df = pd.DataFrame()
                totals_df = totals_df.append(totals_row, ignore_index=True)
                totals_df.reset_index(inplace=True)
                totals_df.rename(columns={'index': 'Name'}, inplace=True)
                totals_df['Name'] = 'Total'

                totals_df[['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL', 'PL_D10U5', 'PL_U5U3', 'PinPout', 'Actual', 'ExpOptVal', 'With_Exch']] = totals_df[
                    ['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL', 'PL_D10U5', 'PL_U5U3', 'PinPout', 'Actual', 'ExpOptVal', 'With_Exch']].astype(int)

                pnl_df[['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL', 'PL_D10U5', 'PL_U5U3', 'PinPout', 'Actual', 'ExpOptVal', 'With_Exch']] = pnl_df[
                    ['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL', 'PL_D10U5', 'PL_U5U3', 'PinPout', 'Actual', 'ExpOptVal', 'With_Exch']].astype(int)


                # totals_df = totals_df.astype(float).round(2)
                # pnl_df = pnl_df.astype(float).round(2)

                # totals_df[['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL', 'PL_D10U5', 'PL_U5U3', 'PinPout', 'Actual',
                #      'ExpOptVal', 'With_Exch']] = round(totals_df[['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL', 'PL_D10U5', 'PL_U5U3', 'PinPout', 'Actual', 'ExpOptVal', 'With_Exch']], 2)
                #
                # pnl_df[
                #     ['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL', 'PL_D10U5', 'PL_U5U3', 'PinPout', 'Actual',
                #      'ExpOptVal', 'With_Exch']] = round(pnl_df[['Mrg', 'Y_PNL', 'E_PNL', 'O_PNL', 'I_PNL', 'T_PNL',
                #                                                    'PL_D10U5', 'PL_U5U3', 'PinPout', 'Actual',
                #                                                    'ExpOptVal', 'With_Exch']], 2)
                #

                totals_styled_df = style_dataframe(totals_df)
                pnl_styled_df = style_dataframe(pnl_df)

                total_dataframe_placeholder.dataframe(totals_styled_df, width=5000)
                pnl_dataframe_placeholder.dataframe(pnl_styled_df, height=1350, width=5000)

            # Sleep for 3 seconds before the next update
            time.sleep(3)



if __name__ == "__main__":
    main()


