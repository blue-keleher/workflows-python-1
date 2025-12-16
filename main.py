from render_sdk.workflows import task, start, Options, Retry
import asyncio
import random

# A minimal task definition
@task
def calculate_square(a: int) -> int:
  return a * a

# A task that runs two parallel subtasks
# (Must be async to await subtask results)
@task
async def sum_squares(a: int, b: int) -> int:
  result1, result2 = await asyncio.gather(
    calculate_square(a),
    calculate_square(b)
  )
  return result1 + result2

# A task that flips a coin and retries on "tails"
# (Illustrates specifying retry logic on failure)
@task(
  options=Options(
    retry=Retry(
      max_retries=3, # Retry up to 3 times (i.e., 4 total attempts)
      wait_duration_ms=1000, # Set a base retry delay of 1 second
      factor=1.5 # Increase delay by 50% after each retry (exponential backoff)
    )
  )
)
def flip_coin() -> str:
  if random.random() < 0.5:
    raise Exception("Flipped tails! Retrying.")
  return "Flipped heads!"

# A task for testing calling with named arguments
@task
def concat_strings(first: str, second: str) -> str:
  return first + second

@task
async def concat_strings_parent(a: str, b: str, c: str, d: str) -> str:
  s1, s2 = await asyncio.gather(
    concat_strings(second=a, first=b),
    concat_strings(second=c, first=d)
  )
  return concat_strings(second=s1, first=s2)

# A task with a default argument
@task
def calculate_square_with_default(a: int = 1) -> int:
  return a * a

if __name__ == "__main__":
  start() # SDK entry point, required for all workflow services
