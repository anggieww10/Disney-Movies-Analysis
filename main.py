import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
def load_data():
    data = pd.read_csv('disney_movies.csv')
    data['release_date'] = pd.to_datetime(data['release_date'], errors='coerce')
    data['year'] = data['release_date'].dt.year
    data['genre'] = data['genre'].fillna('Unknown')
    data['mpaa_rating'] = data['mpaa_rating'].fillna('Not Rated')
    data['total_gross'] = pd.to_numeric(data['total_gross'], errors='coerce')
    data['inflation_adjusted_gross'] = pd.to_numeric(data['inflation_adjusted_gross'], errors='coerce')
    return data

df = load_data()

# Streamlit App
def main():
    st.title("Disney Movies Visualization")
    st.markdown("""
    This application provides an interactive exploration of Disney movies' dataset. 
    Use the filters and visualizations to explore the data!
    """)

    # Sidebar for filters
    st.sidebar.header("Filters")

    genres = st.sidebar.multiselect(
        "Select Genre(s):", options=df['genre'].unique(), default=df['genre'].unique()
    )

    ratings = st.sidebar.multiselect(
        "Select MPAA Rating(s):", options=df['mpaa_rating'].unique(), default=df['mpaa_rating'].unique()
    )

    years = st.sidebar.slider(
        "Select Year Range:",
        int(df['year'].min()),
        int(df['year'].max()),
        (int(df['year'].min()), int(df['year'].max()))
    )

    filtered_df = df.copy()

    gross_range = st.sidebar.slider(
        "Select Total Gross Range:",
        int(filtered_df['total_gross'].min()), int(filtered_df['total_gross'].max()),
        (int(filtered_df['total_gross'].min()), int(filtered_df['total_gross'].max()))
    )
    
    filtered_df = filtered_df[
        (filtered_df['genre'].isin(genres)) &
        (filtered_df['mpaa_rating'].isin(ratings)) &
        (filtered_df['year'].between(years[0], years[1])) &
        (filtered_df['total_gross'] >= gross_range[0]) &
        (filtered_df['total_gross'] <= gross_range[1])
    ]

    search_term = st.sidebar.text_input("Search Movie Title:")
    if search_term:
        filtered_df = filtered_df[filtered_df['movie_title'].str.contains(search_term, case=False, na=False)]

    # Display filtered data
    st.subheader("Filtered Data")
    if not filtered_df.empty:
        st.dataframe(filtered_df)
    else:
        st.write("No data available for the selected filters.")

    # Visualizations
    if not filtered_df.empty:
        st.subheader("Visualizations")

        # 1. Total Energy Generation Visualization (Improved Stacked Area Chart)
        st.markdown("### Total Gross by Genre Over Time")
        if 'genre' in filtered_df.columns and 'total_gross' in filtered_df.columns:
            fig = px.area(
                filtered_df,
                x='year',
                y='total_gross',
                color='genre',
                line_group='genre',
                hover_data={"total_gross": True, "genre": True},
                title="Interactive Total Gross by Genre Over Time",
                labels={"total_gross": "Total Gross (in Millions)", "year": "Year"}
            )
            fig.update_traces(mode="lines+markers", hovertemplate=None)
            st.plotly_chart(fig)

        # 2. Distribution of Movies by Genre
        st.markdown("### Distribution of Movies by Genre")
        fig1 = px.pie(filtered_df, names='genre', title="Distribution of Movies by Genre")
        fig1.update_traces(textinfo='percent+label')
        st.plotly_chart(fig1)

        # 3. Total Gross Trend by Year
        st.markdown("### Total Gross Trend by Year")
        yearly_gross = filtered_df.groupby('year')[['total_gross']].sum().reset_index()
        fig2 = px.line(yearly_gross, x='year', y='total_gross', title="Total Gross Trend by Year")
        fig2.update_layout(hovermode='x unified')
        st.plotly_chart(fig2)

        # 4. Static Visualization with Year Slider
        st.markdown("### Inflation Adjusted Gross by Year")
        selected_year = st.slider("Select Year", int(filtered_df['year'].min()), int(filtered_df['year'].max()), int(filtered_df['year'].min()))
        filtered_year_df = filtered_df[filtered_df['year'] == selected_year]

        fig4 = px.scatter(
            filtered_year_df,
            x='genre',
            y='inflation_adjusted_gross',
            size='total_gross',
            color='genre',
            hover_name='movie_title',
            title=f"Inflation Adjusted Gross for Year {selected_year}",
        )
        st.plotly_chart(fig4)

        # 5. Barplot: Total Gross by MPAA Rating
        st.markdown("### Total Gross by MPAA Rating")
        rating_gross = filtered_df.groupby('mpaa_rating')[['total_gross']].sum().reset_index()
        fig5 = px.bar(
            rating_gross,
            x='mpaa_rating',
            y='total_gross',
            color='mpaa_rating',
            title="Total Gross by MPAA Rating",
            labels={"total_gross": "Total Gross (in Millions)", "mpaa_rating": "MPAA Rating"}
        )
        fig5.update_layout(xaxis_title="MPAA Rating", yaxis_title="Total Gross")
        st.plotly_chart(fig5)

    st.markdown("---")
    st.markdown("**Designed by [Kelompok 15]**")

if __name__ == "__main__":
    main()


st.title("Laporan")
st.markdown("""Visualisasi ini bertujuan untuk memenuhi tugas Visualisasi Data. Visualisasi dibuat interaktif berdasarkan dataset film Disney. Pembuatan visualisasi ini memanfaatkan streamlit dan plotly yang merupakan liblary python. Berbagai aspek data dapat di eksplorasi pengguna seperti total pendapatan berdasarkan genre, distibusi genre dan juga pendapatan disesuaikan inflasi.

Alasan pembuatan desain:

	1. Pada sidebar terdapat filter interaktif, ini bertujuan memudahkan pengguna untuk memfokuskan eksplorasi pada subset data tertentu. Filter interaktif ini mencakup multiselect yang dapa memungkinkan pengguna untuk memelih beberapa genre atau rating. Selain itu, ada slider yang memungkinkan eksplorasi dalam rentang tahun dan pendapatan tertentu. Kemudian, ada search bar yang memudahkan pengguna dalam mencari judul film secara spesifik.

	2. Visualisasi dibuat beragam sesuai dengan fungsinya masing-masing. Pie-chart digunakan untuk menampilkan distribusi genre menggunakan persentase. Tren pendapatan genre berdasarkan waktu dapat ditampilkan menggunakan Area-chart. Line-chart yang digunakan untuk menampilkan total pendapatan pertahun. Dalam pembandingan data inflasi terhadap genre untuk tahun-tahun tertentu dapat di visualisasikan mengguhakan Scatter-plot. Kemudian yang terakhir, Bar-chart digunakan untuk menyediakan komparasi pendatapapn total berdasarkan rating MPAA.

	3. Warna-warna yang di tampilkan pada visualisasi ini berbeda-beda agar lebih mudah untuk diferensiasi. Selain itu, penyesuaian pada spasi dan margin juga dilakukan guna visualisasi yang tidak padat.

Proses Pengembangan:
1. Dataset
	Pada langkah ini, dataset dipersiapkan dengan meload dataset menggunakan Pandas. Kemudian menghandel missing value dengan mengisi data kosong dengan "Unknown" dan "Not Rated". Tidak hanya itu, konversi juga dilakukan pada kolom total_gross dan inflation_adjusted_gross menjadi nilai numerik untuk keperluan visualisasi.

2. Filter
	Filter dilakukan berdasarkan genre, rating, entang tahun, dan rentang pendapatan. Filter dibuat dengan menggunakan elemen interaktif Streamlit seperti slider dan multiselect.

3. Pengimplementasian visualisasi
	- visualisasi yang interaktif dibuat menggunakan plotly.
	- hover tooltip digunakan pada setiap grafik agar pengguna mendapatkan informasi tambahan.

4. Penyesuaian Margin dan Tata Letak:
        - jaral antar visualisasi ditambahkan dengan st.markdown("<br>", unsafe_allow_html=True).


Sumber:
Library yang digunakan: Untuk antarmuka pengguna, visualisasi ini menggunakan streamlit
Plotly Express: Untuk visualisasi.
Pandas: digunakan untuk memanipulasi data.
Dataset: Dataset yang digunakan merupakan dataset film Disney umum digunakan untuk analisis eksplorasi.
    """)
