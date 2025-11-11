import hydra, wandb
from omegaconf import DictConfig
from rsvp_stack.stack import RSVPStack

@hydra.main(version_base=None, config_path="configs", config_name="config")
def train(cfg: DictConfig):
    wandb.init(project="RSVP-Stack", config=cfg, reinit=True)
    stack = RSVPStack(cfg)
    results = stack.run()
    if 'rsvp' in results and isinstance(results['rsvp'], dict):
        wandb.log({'rsvp_coherence_len': len(results['rsvp'].get('coherence', []))})
    wandb.finish()

if __name__ == "__main__":
    train()
