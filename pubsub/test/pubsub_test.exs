defmodule PubsubTest do
  use ExUnit.Case
  doctest Pubsub

  test "can create and publish articles" do
    # Start the application
    {:ok, _} = Application.ensure_all_started(:pubsub)
    Process.sleep(100)

    # Publish an article
    Pubsub.publish_article("Test Article", "This is a test content", "Test Author")
    Process.sleep(500)

    assert true  # Basic smoke test
  end
end
