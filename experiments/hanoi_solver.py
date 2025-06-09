def tower_of_hanoi(n: int, source: str, auxiliary: str, target: str, move_count: list, pass_through_count: list) -> None:
    """Solve Tower of Hanoi recursively, tracking moves and pass-throughs."""
    if n == 0:
        return
    
    # Move n-1 disks from source to auxiliary, using target as auxiliary
    tower_of_hanoi(n - 1, source, target, auxiliary, move_count, pass_through_count)
    
    # Move the nth disk from source to target
    move_count[0] += 1
    is_pass_through = (source != "source" and target != "target") or \
                     (source != "target" and target != "source")
    if is_pass_through:
        pass_through_count[0] += 1
        print(f"Move {move_count[0]}: Disk {n} from {source} to {target} (passing through)")
    else:
        print(f"Move {move_count[0]}: Disk {n} from {source} to {target}")
    
    # Move n-1 disks from auxiliary to target, using source as auxiliary
    tower_of_hanoi(n - 1, auxiliary, source, target, move_count, pass_through_count)

def main(n: int) -> None:
    """Run Tower of Hanoi solver for n disks."""
    print(f"Initial state: {{'source': {list(range(1, n + 1))[::-1]}, 'auxiliary': [], 'target': []}}")
    move_count = [0]  # Mutable to track moves across recursion
    pass_through_count = [0]  # Track pass-through moves
    tower_of_hanoi(n, "source", "auxiliary", "target", move_count, pass_through_count)
    print(f"Solution complete in {move_count[0]} moves.")
    print(f"Number of pass-through moves: {pass_through_count[0]}")
    print(f"Final state: {{'source': [], 'auxiliary': [], 'target': {list(range(1, n + 1))[::-1]}}}")

if __name__ == "__main__":
    n = 10  # Number of disks
    main(n)
