import pandas as pd
import streamlit as st


def carregar_historico():
    return pd.read_csv("vagas_historico.csv")


def filtrar(df, cargo, modalidades, status, apenas_sp_ou_remoto):
    if cargo:
        df = df[df["Título"].str.lower().str.contains(cargo.lower(), na=False)]

    if modalidades:
        df = df[df["Modelo"].isin(modalidades)]

    if status:
        df = df[df["status"].isin(status)]

    if apenas_sp_ou_remoto:
        df = df[(df["Estado"] == "SP") | (df["Modelo"].str.contains("Remoto", na=False))]

    return df


def main():
    st.set_page_config(page_title="Histórico de Vagas Gupy", layout="wide")
    st.title("Histórico de Vagas da Gupy (70 empresas)")

    cargo = st.sidebar.text_input("Cargo desejado", value="Infraestrutura")

    modalidades = st.sidebar.multiselect(
        "Modalidade",
        ["Remoto", "Híbrido", "Presencial"],
        default=["Remoto", "Híbrido", "Presencial"]
    )

    status = st.sidebar.multiselect(
        "Status da vaga",
        ["nova", "ativa", "removida"],
        default=["nova", "ativa"]
    )

    apenas_sp_ou_remoto = st.sidebar.checkbox("Somente SP ou Remoto", value=True)

    buscar = st.sidebar.button("Carregar histórico")

    if buscar:
        try:
            df = carregar_historico()
        except FileNotFoundError:
            st.error("Arquivo vagas_historico.csv não encontrado. Rode o coletor primeiro.")
            return

        df = filtrar(df, cargo, modalidades, status, apenas_sp_ou_remoto)

        st.subheader(f"Total de vagas encontradas: {len(df)}")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("📥 Baixar CSV", csv, "vagas_filtradas.csv", "text/csv")


if __name__ == "__main__":
    main()
