from flask import Flask, render_template, request
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import matplotlib

matplotlib.use('Agg')

app = Flask(__name__)

try:
    df = pd.read_csv('drone_logs.csv')
except:
    df = pd.DataFrame({'Hata': [0]})

# 2. İsim Haritası (Mapping)
column_map = {
    'Ucus_Suresi_dk': 'Uçuş Süresi (Dakika)',
    'Batarya_Seviyesi': 'Batarya Seviyesi (%)',
    'Yukseklik_m': 'İrtifa (Metre)',
    'Hiz_ms': 'Hız (m/s)',
    'Sinyal_Gucu_dBm': 'Sinyal Gücü (dBm)',
    'Motor_Sicakligi_C': 'Motor Sıcaklığı (°C)'
}
reverse_map = {v: k for k, v in column_map.items()}

@app.route('/', methods=['GET', 'POST'])
def index():
    readable_columns = list(column_map.values())
    selected_x_label = readable_columns[0]
    selected_y_label = readable_columns[1]
    plot_url = None
    insight = ""
    graph_type = "scatter" 

    if request.method == 'POST':
        selected_x_label = request.form.get('x_col')
        selected_y_label = request.form.get('y_col')
        graph_type = request.form.get('graph_type')
        
        tech_x = reverse_map[selected_x_label]
        tech_y = reverse_map[selected_y_label]

        # --- GRAFİK ÇİZİM MOTORU ---
        plt.figure(figsize=(11, 7))
        plt.style.use('dark_background')
        
        if graph_type == 'heatmap':
            # === MOD 1: ISI HARİTASI (HEATMAP) ===
            corr_matrix = df.rename(columns=column_map).corr()
            
             
            sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', 
                        linewidths=0.5, linecolor='#1e2332',
                        cbar_kws={'label': 'Korelasyon Katsayısı'})
            
            plt.title('Tüm Parametrelerin Korelasyon Analizi', color='#00d4ff', fontsize=16)
            insight = "🔥 Sistem Taraması: Kırmızı alanlar doğru orantıyı, mavi alanlar ters orantıyı gösterir."
            
        else:
            
            sns.scatterplot(data=df, x=tech_x, y=tech_y, 
                            hue='Yukseklik_m', palette='viridis', s=120, alpha=0.9, edgecolor='white')
            
            plt.title(f'{selected_x_label} vs {selected_y_label}', color='#00d4ff', fontsize=16)
            plt.xlabel(selected_x_label, color='white', fontsize=12)
            plt.ylabel(selected_y_label, color='white', fontsize=12)
            plt.grid(True, linestyle='--', alpha=0.2)
            
            corr = df[tech_x].corr(df[tech_y])
            if corr < -0.6:
                insight = "⚠️ Analiz: Güçlü TERS orantı tespit edildi. Biri artarken diğeri azalıyor."
            elif corr > 0.6:
                insight = "✅ Analiz: Güçlü DOĞRU orantı tespit edildi. Parametreler senkronize."
            else:
                insight = "ℹ️ Analiz: Parametreler arasında belirgin bir doğrusal ilişki yok."

        plt.tight_layout()

        # Resmi Base64'e çevir
        img = io.BytesIO()
        plt.savefig(img, format='png', transparent=True)
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()

    # --- İSTATİSTİK TABLOSU ---
    df_display = df.rename(columns=column_map)
    desc_df = df_display.describe()
    # Türkçeleştirme.
    row_translation = {
        'count': 'Veri Sayısı', 'mean': 'Ortalama', 'std': 'Std. Sapma',
        'min': 'Minimum', '25%': '%25 (Q1)', '50%': 'Medyan', 
        '75%': '%75 (Q3)', 'max': 'Maksimum'
    }
    desc_df = desc_df.rename(index=row_translation)

    summary_table = desc_df.to_html(classes='table table-dark table-hover table-striped', float_format='%.2f')

    return render_template('index.html', 
                           columns=readable_columns, 
                           selected_x=selected_x_label, 
                           selected_y=selected_y_label, 
                           plot_url=plot_url, 
                           summary_table=summary_table,
                           insight=insight,
                           graph_type=graph_type)

if __name__ == '__main__':
    app.run(debug=True)