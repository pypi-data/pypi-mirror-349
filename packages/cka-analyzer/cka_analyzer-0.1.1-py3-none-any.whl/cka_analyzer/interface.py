from cka_analyzer.model import get_device, load_model, load_tokenizer
from cka_analyzer.data import build_dataloader
from cka_analyzer.compute import compute_cka_similarity
from cka_analyzer.plot import plot_cka_single_line

def run_cka_analysis(
    model_reference_path: str,
    model_path: str,
    texts: list[str],
    output_path: str,
    batch_size: int = 4,
    num_batches: int = 10,
    max_length: int = 128
):
    device = get_device()
    tokenizer = load_tokenizer(model_reference_path)
    model_ref = load_model(model_reference_path, device)
    model_upd = load_model(model_path, device)

    dataloader = build_dataloader(
        texts=texts,
        tokenizer=tokenizer,
        model=model_ref,
        batch_size=batch_size,
        max_length=max_length,
        shuffle=False
    )

    num_layers = len(model_ref.model.layers)
    layers = list(range(num_layers))
    cka_results = compute_cka_similarity(
        model_ref=model_ref,
        model_upd=model_upd,
        layers=layers,
        dataloader=dataloader,
        num_batches=num_batches
    )

    plot_cka_single_line(
        cka_results=cka_results,
        layers=layers,
        output_path=output_path,
        label="Updated"
    )
