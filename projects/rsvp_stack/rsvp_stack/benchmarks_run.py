from rsvp_stack.modules import rsvp_torch, ebssc_torch
def run():
    print('Running small benchmarks...')
    h = rsvp_torch.train(None)
    print('RSVP history keys:', list(h.keys()))
    e = ebssc_torch.train(None)
    print('EBSSC result keys:', list(e.keys()))
if __name__=='__main__':
    run()
