import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import pdfkit


def generate_descriptive_tables(df):
    html_sections = []

    # Extended numeric description
    numeric_df = df.select_dtypes(include='number')
    num_stats = numeric_df.describe().T
    num_stats['median'] = numeric_df.median()
    num_stats['skew'] = numeric_df.skew()
    num_stats['kurtosis'] = numeric_df.kurtosis()
    num_stats['iqr'] = numeric_df.quantile(0.75) - numeric_df.quantile(0.25)
    num_stats = num_stats.round(2)
    html_sections.append("<h2>🔢 Descriptive Statistics (Numeric)</h2>")
    html_sections.append(num_stats.to_html())

    # Categorical summary
    cat_df = df.select_dtypes(include='object')
    if not cat_df.empty:
        cat_summary = pd.DataFrame({
            "count": cat_df.count(),
            "unique": cat_df.nunique(),
            "top": cat_df.mode().iloc[0],
            "freq": cat_df.apply(lambda x: x.value_counts().iloc[0] if not x.value_counts().empty else None)
        })
        html_sections.append("<h2>🔤 Descriptive Statistics (Categorical)</h2>")
        html_sections.append(cat_summary.to_html())

    return html_sections


def generate_eda_summary(df):
    lines = []
    num_cols = df.select_dtypes(include='number').columns
    cat_cols = df.select_dtypes(include='object').columns

    lines.append(f"<p><b>Total Rows:</b> {len(df)}</p>")
    lines.append(f"<p><b>Numeric Columns:</b> {len(num_cols)}</p>")
    lines.append(f"<p><b>Categorical Columns:</b> {len(cat_cols)}</p>")
    lines.append(f"<p><b>Total Missing Values:</b> {df.isnull().sum().sum()}</p>")
    lines.append(f"<p><b>Duplicate Rows:</b> {df.duplicated().sum()}</p>")

    missing_percent = df.isnull().mean() * 100
    missing_table = missing_percent[missing_percent > 0].round(1).to_frame(name="Missing (%)")
    if not missing_table.empty:
        lines.append("<h4>Feature-wise Missing %</h4>")
        lines.append(missing_table.to_html())

    corr = df[num_cols].corr()
    high_corr_pairs = (
        corr.where(~np.eye(corr.shape[0], dtype=bool))
        .stack()
        .reset_index()
        .rename(columns={0: "Corr"})  # ✅ Rename before .query
        .query("abs(Corr) > 0.9 and abs(Corr) < 1.0")
    )
    if not high_corr_pairs.empty:
        lines.append("<h4>⚠️ Highly Correlated Features (|r| > 0.9)</h4>")
        lines.append(high_corr_pairs.rename(columns={0: "Correlation"}).to_html(index=False))

    return "<h2>📊 Exploratory Data Analysis Summary</h2>" + "".join(lines)






def generate_univariate_plots(df):
    figs = []
    numeric_cols = df.select_dtypes(include='number').columns

    for col in numeric_cols:
        figs.append(px.histogram(df, x=col, nbins=30, title=f"Histogram of {col}")
                    .to_html(full_html=False, include_plotlyjs='cdn'))
        figs.append(px.box(df, y=col, title=f"Boxplot of {col}")
                    .to_html(full_html=False, include_plotlyjs='cdn'))

    return figs

def generate_categorical_plots(df):
    figs = []
    cat_cols = df.select_dtypes(include='object').columns

    for col in cat_cols:
        vc = df[col].value_counts().nlargest(10)
        fig = px.bar(x=vc.index, y=vc.values, labels={'x': col, 'y': 'Count'}, title=f"Top Categories: {col}")
        fig.update_layout(xaxis_tickangle=45)
        figs.append(fig.to_html(full_html=False, include_plotlyjs='cdn'))

        freq_table_html = vc.to_frame().to_html()
        figs.append(f"<h4>Frequency Table for {col}</h4>{freq_table_html}<br><br>")

    return figs

def generate_missing_value_plot(df):
    null_counts = df.isnull().sum()
    null_counts = null_counts[null_counts > 0]
    if null_counts.empty:
        return ["<p>No missing values in dataset.</p>"]

    fig = px.bar(x=null_counts.index, y=null_counts.values,
                 labels={"x": "Column", "y": "Missing Count"},
                 title="Missing Value Count per Column")
    fig.update_layout(xaxis_tickangle=45)
    return [fig.to_html(full_html=False, include_plotlyjs='cdn')]

def generate_bivariate_plots(df):
    figs = []
    numeric_cols = df.select_dtypes(include='number').columns
    corr = df[numeric_cols].corr().round(2)

    heatmap = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.index,
        colorscale='Viridis'
    ))
    heatmap.update_layout(title="Correlation Heatmap")
    figs.append(heatmap.to_html(full_html=False, include_plotlyjs='cdn'))

    correlated_pairs = (
        corr.where(~np.eye(corr.shape[0], dtype=bool))
        .stack()
        .reset_index()
        .rename(columns={"level_0": "Var1", "level_1": "Var2", 0: "Corr"})
    )
    top_pairs = correlated_pairs[correlated_pairs["Corr"].abs() > 0.7].sort_values(by="Corr", ascending=False)
    seen = set()
    for _, row in top_pairs.iterrows():
        pair = tuple(sorted((row["Var1"], row["Var2"])))
        if pair in seen:
            continue
        seen.add(pair)
        fig = px.scatter(df, x=row["Var1"], y=row["Var2"], trendline="ols",
                         title=f"Scatter: {row['Var1']} vs {row['Var2']} (Corr={row['Corr']:.2f})")
        figs.append(fig.to_html(full_html=False, include_plotlyjs='cdn'))

    return figs






def create_report_html(summary_html, plots_html, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Data Analysis Report</title>
            <meta charset="utf-8">
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{ font-family: Arial; padding: 20px; max-width: 1000px; margin: auto; }}
                h1, h2, h3 {{ color: #2c3e50; }}
                .plot {{ margin-bottom: 40px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
        <h1>📊 Data Profiling Report</h1>
        <h2>Summary Statistics</h2>
        {summary_html}
        <hr>
        {"".join(f'<div class="plot">{plot}</div>' for plot in plots_html)}
        </body></html>
        """)

def export_pdf(html_path, pdf_path):
    try:
        pdfkit.from_file(html_path, pdf_path)
        print(f"📄 PDF saved to: {pdf_path}")
    except Exception as e:
        print("⚠️ PDF export failed:", e)

def generate_report_from_excel(excel_path, output_html="report.html", output_pdf="report.pdf"):
    df = pd.read_excel(excel_path)
    numeric_cols = df.select_dtypes(include='number').columns

    summary_stats = df[numeric_cols].describe().transpose().round(2)
    summary_html = summary_stats.to_html(classes="summary", border=0)
    eda_html = generate_eda_summary(df)
    desc_html = generate_descriptive_tables(df)
    plots = []
    plots += generate_missing_value_plot(df)
    plots += generate_univariate_plots(df)
    plots += generate_categorical_plots(df)
    plots += generate_bivariate_plots(df)



    #create_report_html(summary_html, plots, output_html)
    create_report_html(summary_html, desc_html + [eda_html] + plots, output_html)

    export_pdf(output_html, output_pdf)
    print(f"✅ Report saved to {output_html}")
