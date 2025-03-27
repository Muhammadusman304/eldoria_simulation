from simulation import EldoriaSimulation
import time


def main():
    print("Welcome to Eldoria Treasure Hunt Simulation!")
    width = int(input("Enter grid width (default 20): ") or 20)
    height = int(input("Enter grid height (default 20): ") or 20)

    sim = EldoriaSimulation(width, height)

    print("\nInitial grid:")
    sim.grid.display()

    auto_mode = input("Run automatically? (y/n): ").lower() == 'y'
    max_steps = 100 if auto_mode else 0

    step_count = 0
    while sim.is_running() and (not max_steps or step_count < max_steps):
        if not auto_mode:
            input("\nPress Enter for next step...")

        sim.step()
        step_count += 1

        print(f"\nStep {step_count}:")
        sim.grid.display()

        stats = sim.get_stats()
        print(
            f"\nStats: Active Hunters: {stats['active_hunters']}, Treasures: {stats['treasures']}, Collected: {stats['collected_treasures']}")

        if auto_mode:
            time.sleep(0.5)

    print("\nSimulation ended!")
    final_stats = sim.get_stats()
    print(f"Final stats after {final_stats['steps']} steps:")
    print(f"- Total hunters: {final_stats['hunters']} (active: {final_stats['active_hunters']})")
    print(f"- Knights: {final_stats['knights']}")
    print(f"- Treasures remaining: {final_stats['treasures']}")
    print(f"- Treasures collected: {final_stats['collected_treasures']}")
    print(f"- Hideouts: {final_stats['hideouts']}")


if __name__ == "__main__":
    main()

