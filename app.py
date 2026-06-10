import gradio as gr
from query import ask

def handle_query(question):
    if not question.strip():
        return "Please input a valid question.", ""
    
    result = ask(question)
    answer_text = result["answer"]
    
    # Nicely print the tracking elements beneath the interface window
    if "I don't have enough information on that." in answer_text:
        source_display = "None (Context insufficient)"
    else:
        source_display = "\n".join(f"• {s}" for s in result["sources"])
        
    return answer_text, source_display

# Constructing the layout workspace wrapper
with gr.Blocks(title="The Unofficial UCI CS Guide") as demo:
    gr.Markdown("# 🔱 The Unofficial UCI Course Guide Assistant")
    gr.Markdown("Search grounded advisor insights regarding lower-division computer science courses.")
    
    with gr.Row():
        inp = gr.Textbox(
            label="Your Question", 
            placeholder="e.g., What are the grading penalties on Professor Klefstad's homework quizzes?",
            lines=2
        )
    
    with gr.Column():
        answer = gr.Textbox(label="Grounded Answer Response", lines=8, interactive=False)
        sources = gr.Textbox(label="Retrieved Reference Sources", lines=4, interactive=False)
        
    btn = gr.Button("Submit Query Pipeline", variant="primary")
    
    # Hook triggers for submission routines
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    print("To shut down the app and stop the server, press: Control + C")
    demo.launch(server_name="127.0.0.1", server_port=7860)