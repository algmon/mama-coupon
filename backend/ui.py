import gradio as gr
import user_management as um

iface = gr.Interface(
    fn=um.login_user_to_db,
    inputs=[
        gr.Textbox(label="Database", type="text"),
        gr.Textbox(label="Username", type="text"),
        gr.Textbox(label="Password", type="password"),
    ],
    outputs="text",
    title="User Login",
    description="Simple user login interface.",
)

iface.launch(share=True)