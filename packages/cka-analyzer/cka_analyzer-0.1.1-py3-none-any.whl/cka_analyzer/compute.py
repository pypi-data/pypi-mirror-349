import numpy as np
import torch

def center_gram(K):
    n = K.shape[0]
    unit = np.ones((n, n)) / n
    return K - unit @ K - K @ unit + unit @ K @ unit

def linear_cka(X, Y):
    Xc = X - X.mean(0, keepdims=True)
    Yc = Y - Y.mean(0, keepdims=True)
    Kx, Ky = Xc @ Xc.T, Yc @ Yc.T
    hsic = np.trace(center_gram(Kx) @ center_gram(Ky))
    denom = np.sqrt(
        np.trace(center_gram(Kx) @ center_gram(Kx)) *
        np.trace(center_gram(Ky) @ center_gram(Ky)) + 1e-12
    )
    return float(hsic / denom)

def extract_activations(model, layers_to_analyze, dataloader, num_batches):
    """
    Extract [CLS] or token-0 activations from specified layers.
    """
    activations = {}
    for layer in layers_to_analyze:
        buf = []

        def hook_fn(module, inp, out):
            t = out[0] if isinstance(out, tuple) else out
            buf.append(t[:, 0, :].float().detach().cpu().numpy())

        handle = dict(model.named_modules())[f"model.layers.{layer}"].register_forward_hook(hook_fn)

        with torch.no_grad():
            for i, batch in enumerate(dataloader):
                if i >= num_batches:
                    break
                model(batch["input_ids"])

        handle.remove()
        activations[layer] = np.concatenate(buf, axis=0)

    return activations

def compute_cka_similarity(model_ref, model_upd, layers, dataloader, num_batches):
    """
    Return a dictionary of layer-wise CKA between reference and updated model.
    """
    ref_acts = extract_activations(model_ref, layers, dataloader, num_batches)
    upd_acts = extract_activations(model_upd, layers, dataloader, num_batches)

    return {
        layer: linear_cka(ref_acts[layer], upd_acts[layer])
        for layer in layers
    }
