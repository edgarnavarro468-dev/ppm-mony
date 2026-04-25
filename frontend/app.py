# app.py - Frontend mejorado para PPM (Finanzas Sociales)
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="PPM - Finanzas Sociales",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración de la API
API_URL = "http://localhost:8000"

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .balance-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .expense-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .social-feed {
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
    }
    .feed-item {
        background: white;
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 3px solid #764ba2;
        animation: slideIn 0.3s ease;
    }
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    .stat-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state para el feed social
if 'social_feed' not in st.session_state:
    st.session_state.social_feed = []

def add_to_feed(message, type="info"):
    """Agrega un evento al feed social"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.social_feed.insert(0, {
        "message": message,
        "type": type,
        "time": timestamp
    })
    # Mantener solo últimas 50 entradas
    st.session_state.social_feed = st.session_state.social_feed[:50]

def call_api(endpoint, method="GET", data=None):
    """Función helper para llamar a la API"""
    try:
        if method == "GET":
            response = requests.get(f"{API_URL}{endpoint}")
        elif method == "POST":
            response = requests.post(f"{API_URL}{endpoint}", json=data)
        else:
            return None
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error en la API: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

# Header principal
st.markdown("""
<div class="main-header">
    <h1 style="margin:0">💰 PPM - Finanzas Sociales</h1>
    <p style="margin:0; opacity:0.9">Maneja dinero entre amigos sin dramas</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Navegación
with st.sidebar:
    st.image("https://via.placeholder.com/300x100?text=PPM+MONEY", use_container_width=True)
    st.markdown("## 📊 Navegación")
    page = st.radio("", ["🏠 Dashboard", "👥 Grupos", "💸 Gastos", "⚖️ Balances", "📱 Feed Social", "📈 Estadísticas"])
    
    st.markdown("---")
    st.markdown("### ℹ️ Información")
    st.markdown("""
    **Versión:** 2.0  
    **Estado:** Activo  
    **Usuarios:** 3 miembros
    """)
    
    if st.button("🔄 Sincronizar Datos", use_container_width=True):
        st.rerun()

# Página Dashboard
if page == "🏠 Dashboard":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container():
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.markdown("### 💰 Gastos Totales")
            expenses = call_api("/expenses")
            total_expenses = sum(e.get('amount', 0) for e in expenses) if expenses else 0
            st.markdown(f'<p class="stat-number">${total_expenses:,.2f}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.markdown("### 👥 Grupos Activos")
            groups = call_api("/groups")
            total_groups = len(groups) if groups else 0
            st.markdown(f'<p class="stat-number">{total_groups}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        with st.container():
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.markdown("### 📝 Transacciones")
            expenses = call_api("/expenses")
            total_transactions = len(expenses) if expenses else 0
            st.markdown(f'<p class="stat-number">{total_transactions}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Gastos Recientes")
        if expenses:
            df_expenses = pd.DataFrame(expenses)
            df_expenses['amount'] = df_expenses['amount'].astype(float)
            df_expenses['payer'] = df_expenses['payer'].astype(str)
            df_expenses['description'] = df_expenses['description'].astype(str)
            st.dataframe(df_expenses[['payer', 'amount', 'description']], use_container_width=True)
        else:
            st.info("No hay gastos registrados aún")
    
    with col2:
        st.markdown("### 🎯 Acciones Rápidas")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("➕ Nuevo Gasto", use_container_width=True):
                st.session_state.page = "💸 Gastos"
                st.rerun()
        with col_b:
            if st.button("👥 Crear Grupo", use_container_width=True):
                st.session_state.page = "👥 Grupos"
                st.rerun()

# Página Grupos
elif page == "👥 Grupos":
    st.markdown("## 👥 Gestión de Grupos")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Crear Nuevo Grupo")
        with st.form("create_group_form"):
            group_name = st.text_input("Nombre del grupo", placeholder="Ej: Roomies, Viaje Playa, Amigos")
            submitted = st.form_submit_button("Crear Grupo", use_container_width=True)
            
            if submitted and group_name:
                result = call_api("/add-group", method="POST", data={"name": group_name})
                if result:
                    st.success(f"✅ Grupo '{group_name}' creado exitosamente")
                    add_to_feed(f"Se creó el grupo '{group_name}'", "success")
                    st.rerun()
    
    with col2:
        st.markdown("### Mis Grupos")
        groups = call_api("/groups")
        if groups:
            for group in groups:
                with st.container():
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.markdown(f"**📁 {group['name']}**")
                        st.caption(f"ID: {group['id']}")
                    with col_b:
                        if st.button("Ver Detalles", key=f"btn_{group['id']}"):
                            st.info(f"Detalles del grupo {group['name']} - Próximamente más funciones")
        else:
            st.info("No hay grupos creados aún. ¡Crea tu primer grupo!")

# Página Gastos
elif page == "💸 Gastos":
    st.markdown("## 💸 Registro de Gastos")
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown("### Nuevo Gasto")
        with st.form("add_expense_form"):
            payer = st.selectbox("¿Quién pagó?", ["Edgar", "Diego", "Fernando"])
            amount = st.number_input("Monto ($)", min_value=0.01, step=10.0, format="%0.2f")
            description = st.text_input("Concepto", placeholder="Ej: Cena, Supermercado, Salida")
            
            # Personas que participan
            st.markdown("**¿Entre quiénes se divide?**")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                divide_edgar = st.checkbox("Edgar", value=True)
            with col_b:
                divide_diego = st.checkbox("Diego", value=True)
            with col_c:
                divide_fernando = st.checkbox("Fernando", value=True)
            
            participants = []
            if divide_edgar: participants.append("Edgar")
            if divide_diego: participants.append("Diego")
            if divide_fernando: participants.append("Fernando")
            
            submitted = st.form_submit_button("Registrar Gasto", use_container_width=True, type="primary")
            
            if submitted and amount > 0 and description:
                result = call_api("/add-expense", method="POST", data={
                    "payer": payer,
                    "amount": float(amount),
                    "description": description
                })
                if result:
                    # Calcular cuánto debe cada uno
                    share_per_person = amount / len(participants) if participants else 0
                    st.success(f"✅ Gasto registrado: ${amount:.2f} pagado por {payer}")
                    add_to_feed(f"{payer} pagó ${amount:.2f} por '{description}'", "expense")
                    
                    # Mostrar quién debe qué
                    for p in participants:
                        if p != payer:
                            st.info(f"💸 {p} debe ${share_per_person:.2f} a {payer}")
                    st.rerun()
    
    with col2:
        st.markdown("### Historial de Gastos")
        expenses = call_api("/expenses")
        if expenses:
            # Crear DataFrame para mostrar
            df = pd.DataFrame(expenses)
            df['amount'] = df['amount'].astype(float)
            df['Pagos'] = df['amount'].apply(lambda x: f"${x:,.2f}")
            
            # Mostrar con estilo
            for idx, expense in enumerate(df.to_dict('records')):
                with st.container():
                    st.markdown(f"""
                    <div class="expense-card">
                        <strong>💵 {expense['description']}</strong><br>
                        Pagado por: <strong>{expense['payer']}</strong><br>
                        Monto: <strong style="color:#667eea">${expense['amount']:,.2f}</strong>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No hay gastos registrados. ¡Agrega tu primer gasto!")

# Página Balances
elif page == "⚖️ Balances":
    st.markdown("## ⚖️ Balances y Deudas")
    
    st.markdown("### Calculadora de Deudas")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_amount = st.number_input("Monto total", min_value=0.01, step=50.0, key="balance_total")
    with col2:
        num_people = st.number_input("Número de personas", min_value=1, max_value=10, value=3, key="balance_people")
    with col3:
        st.markdown("### 💰")
        if st.button("Calcular", use_container_width=True):
            if total_amount > 0:
                share = total_amount / num_people
                st.balloons()
                st.markdown(f"""
                <div class="balance-card">
                    <h3>Resultado</h3>
                    <p>Cada persona debe pagar: <strong>${share:.2f}</strong></p>
                    <hr>
                    <p>💡 Si una persona pagó el total:</p>
                    <ul>
                        <li>Las otras {num_people-1} personas deben pagarle <strong>${share:.2f} cada una</strong></li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Resumen de Deudas Actuales")
    
    expenses = call_api("/expenses")
    if expenses:
        # Crear un resumen simple de quién debe qué
        paid_by = {}
        for expense in expenses:
            payer = expense['payer']
            amount = expense['amount']
            paid_by[payer] = paid_by.get(payer, 0) + amount
        
        if paid_by:
            df_balances = pd.DataFrame([{"Persona": k, "Pagó": f"${v:,.2f}"} for k, v in paid_by.items()])
            st.dataframe(df_balances, use_container_width=True, hide_index=True)
        else:
            st.info("Calculando balances...")
    else:
        st.info("No hay gastos registrados para calcular balances")

# Página Feed Social
elif page == "📱 Feed Social":
    st.markdown("## 📱 Feed Social")
    st.caption("Actividad reciente de tu grupo")
    
    # Botón para limpiar feed
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🗑️ Limpiar Feed", use_container_width=True):
            st.session_state.social_feed = []
            st.rerun()
    
    st.markdown("---")
    
    with st.container():
        st.markdown('<div class="social-feed">', unsafe_allow_html=True)
        if st.session_state.social_feed:
            for event in st.session_state.social_feed:
                icon = "💰" if event['type'] == "expense" else "✅" if event['type'] == "success" else "ℹ️"
                st.markdown(f"""
                <div class="feed-item">
                    <small style="color:#764ba2">{event['time']}</small><br>
                    {icon} {event['message']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📭 No hay actividad reciente. ¡Comienza agregando gastos o creando grupos!")
        st.markdown('</div>', unsafe_allow_html=True)

# Página Estadísticas
elif page == "📈 Estadísticas":
    st.markdown("## 📈 Estadísticas y Análisis")
    
    expenses = call_api("/expenses")
    
    if expenses and len(expenses) > 0:
        df = pd.DataFrame(expenses)
        df['amount'] = df['amount'].astype(float)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Gastos por Persona")
            gastos_por_persona = df.groupby('payer')['amount'].sum().reset_index()
            fig = px.pie(gastos_por_persona, values='amount', names='payer', title="Distribución de Gastos")
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Top Gastos")
            top_gastos = df.nlargest(5, 'amount')[['description', 'payer', 'amount']]
            fig = px.bar(top_gastos, x='description', y='amount', color='payer', title="Mayores Gastos")
            fig.update_layout(xaxis_title="Concepto", yaxis_title="Monto ($)")
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### Evolución de Gastos")
        
        # Agregar columna de índice para simular fechas
        df['gasto_num'] = range(1, len(df) + 1)
        fig = px.line(df, x='gasto_num', y='amount', title="Flujo de Gastos", markers=True)
        fig.update_layout(xaxis_title="Número de Gasto", yaxis_title="Monto ($)")
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### Resumen Ejecutivo")
        st.markdown(f"""
        - **Total Gastado:** ${df['amount'].sum():,.2f}
        - **Promedio por Gasto:** ${df['amount'].mean():,.2f}
        - **Gasto más alto:** ${df['amount'].max():,.2f}
        - **Total de transacciones:** {len(df)}
        """)
    else:
        st.info("📊 No hay suficientes datos para mostrar estadísticas. ¡Agrega algunos gastos primero!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>PPM - Finanzas Sociales © 2024 | Maneja dinero entre amigos sin dramas</small>
</div>
""", unsafe_allow_html=True)