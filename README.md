# ACCORD-SL T1/T2 research demo (Streamlit)

Research-use-only T1/T2 batch scoring demonstration for the ACCORD-SL prototype.

- **T1** tab: 20-item low-burden pre-screen + age.
- **T2** tab: 11-item specialist-priority contract + age.
- Fast mode uses two-expert approximations; not a diagnosis and not for clinical use.

## Deploy on Streamlit Community Cloud

1. Go to https://share.streamlit.io and sign in with GitHub.
2. Create a new app from this repository.
3. Main file path: `streamlit_app.py`.
4. Deploy.

Deploy link:

https://share.streamlit.io/deploy?repository=https://github.com/Shadowind111/accord-sl-demo&branch=main&mainModule=streamlit_app.py

## Local run

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## License

Code MIT; model weights CC BY-NC 4.0. No clinical use.
