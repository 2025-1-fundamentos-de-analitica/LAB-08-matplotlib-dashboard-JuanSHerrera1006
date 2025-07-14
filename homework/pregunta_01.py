# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import os

INPUT_PATH = "files/input/"
DOCS_PATH = "docs/"

def create_shipping_per_warehouse_visual(df):
    # New Figure 
    plt.Figure()
    df = df.copy()["Warehouse_block"].value_counts()
    df.plot.bar(
        title="Shipping per Warehouse",
        xlabel="Warehouse block",
        ylabel="Record Count",
        color="tab:blue",
        fontsize=8
    )
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    # Save graph
    plt.savefig(os.path.join(DOCS_PATH, "shipping_per_warehouse.png"))


def create_mode_of_shipment_visual(df):
    # New Figure 
    plt.Figure()

    df = df.copy()["Mode_of_Shipment"].value_counts()
    df.plot.pie(
        title="Mode of shipment",
        wedgeprops=dict(width=0.35),
        ylabel="",
        colors=["tab:blue", "tab:orange", "tab:green"]
    )
    # Save graph
    plt.savefig(os.path.join(DOCS_PATH, "mode_of_shipment.png"))

def create_avg_customer_rating_visual(df):
    # New Figure 
    plt.Figure()

    df = (
        df.copy()[["Mode_of_Shipment", "Customer_rating"]]
        .groupby("Mode_of_Shipment")
        .describe()
    )
    df.columns = df.columns.droplevel()
    df = df[["mean", "min", "max"]]

    plt.barh(
        y=df.index.values,
        width=df["max"].values - 1,
        left=df["min"].values,
        height=0.9,
        color="lightgray",
        alpha=0.8
    )

    colors = [
        "tab:green" if value >= 3.0 else "tab:orange" for value in df["mean"].values
    ]

    plt.barh(
        y=df.index.values,
        width=df["mean"].values - 1,
        left=df["min"].values,
        height=0.5,
        color=colors,
        alpha=1
    )

    plt.title("Average Customer Rating")
    plt.gca().spines["left"].set_color("gray")
    plt.gca().spines["bottom"].set_color("gray")
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    # Save graph
    plt.savefig(os.path.join(DOCS_PATH, "average_customer_rating.png"))\


def create_weight_distribution_visual(df):
    plt.Figure()

    df["Weight_in_gms"].plot.hist(
        title="Shipped Weight Distribution",
        color="tab:orange",
        edgecolor="white"
    )

    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    plt.savefig(os.path.join(DOCS_PATH, "weight_distribution.png"))

def pregunta_01():
    """
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    """
    # Ignored warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    ### Create docs directory
    if not(os.path.exists(DOCS_PATH)):
        os.mkdir(DOCS_PATH)
    
    df = pd.read_csv(os.path.join(INPUT_PATH, "shipping-data.csv"))

    # Create graphs
    create_shipping_per_warehouse_visual(df)
    create_avg_customer_rating_visual(df)
    create_mode_of_shipment_visual(df)
    create_weight_distribution_visual(df)

    # Save HTML dashboard
    html = '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Shipping Dashboard</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
                color: #333;
            }

            header {
                background-color: #007bff;
                color: white;
                padding: 20px;
                text-align: center;
            }

            h1 {
                margin: 0;
                font-size: 36px;
            }

            h2 {
                font-size: 24px;
                color: #333;
                text-align: center;
            }

            .container {
                max-width: 1200px;
                margin: 20px auto;
                padding: 20px;
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                justify-content: space-around;
            }

            figure {
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                overflow: hidden;
                width: 100%;
                max-width: 500px;
                margin: 0;
                padding: 10px;
                text-align: center;
            }

            figure img {
                width: 100%;
                border-radius: 10px;
                max-height: 400px;
                object-fit: cover;
            }

            figure h2 {
                margin-top: 10px;
            }

            @media (max-width: 768px) {
                .container {
                    flex-direction: column;
                    align-items: center;
                }

                figure {
                    width: 90%;
                }
            }
        </style>
    </head>

    <body>
        <header>
            <h1>Shipping Dashboard</h1>
        </header>

        <div class="container">
            <figure>
                <h2>Envíos por Warehouse</h2>
                <img src="shipping_per_warehouse.png" alt="Shipping per Warehouse">
            </figure>
            <figure>
                <h2>Mode of Shipment</h2>
                <img src="mode_of_shipment.png" alt="Mode of Shipment">
            </figure>
            <figure>
                <h2>Average Customer Rating</h2>
                <img src="average_customer_rating.png" alt="Average Customer Rating">
            </figure>
            <figure>
                <h2>Weight Distribution</h2>
                <img src="weight_distribution.png" alt="Weight Distribution">
            </figure>
        </div>
    </body>
    </html>'''

    with open(os.path.join(DOCS_PATH, "index.html"), "w") as file:
        file.write(html)