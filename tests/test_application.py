import kdlc


def test_main(mocker):
    prompt = mocker.MagicMock()
    mocker.patch("kdlc.prompt", new=prompt)

    kdlc.main()
    prompt.assert_called()
