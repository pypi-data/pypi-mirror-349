def main(prompt):
    from huggingface_hub import InferenceClient
    apoo = ['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', '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', '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']
    apoo = iter(apoo)
    while True:
        try:
            client = InferenceClient(
                provider="replicate",
                api_key=next(apoo),
            )

            # output is a PIL.Image object
            image = client.text_to_image(
                f"{prompt}",
                model="stabilityai/stable-diffusion-3.5-large",
            )
            
            return image
            
        except StopIteration as e:
            apoo = iter(apoo)
        except:
            pass


