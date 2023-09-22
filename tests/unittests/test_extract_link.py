def test_extract_link_happy_scenario(bot_instance):
    # Assuming that https://www.youtube.com/watch?v=tx0PoKa7BDs is a valid youtube link
    message = "Check out this cool video: https://www.youtube.com/watch?v=tx0PoKa7BDs !"
    expected_result = "https://www.youtube.com/watch?v=tx0PoKa7BDs"

    # Call the method you are testing
    result = bot_instance.extract_link(message)

    # Assert that the method returns the expected result
    assert result == expected_result, f"Expected {expected_result}, but got {result}"


def test_extract_link_no_link_found(bot_instance):
    # Assuming the message contains no valid YouTube link
    message = "This is a message without any links."

    # Call the method you are testing
    result = bot_instance.extract_link(message)

    # Assert that the method returns None
    assert result is None, f"Expected None, but got {result}"


def test_extract_link_invalid_link(bot_instance):
    # Assuming the message contains a link, but it's not a valid YouTube link
    message = "Check out this site: http://example.com."

    # Call the method you are testing
    result = bot_instance.extract_link(message)

    # Assert that the method returns None
    assert result is None, f"Expected None, but got {result}"
