import hydra, wandb
from omegaconf import DictConfig
from rsvp_stack.stack import RSVPStack

@hydra.main(version_base=None, config_path="configs", config_name="config")
def train(cfg: DictConfig):
    wandb.init(project="RSVP-Stack", config=cfg)
    stack = RSVPStack(cfg)
    results = stack.run()
    wandb.finish()

if __name__ == "__main__":
    train()