import mock

from ocelot.pipeline.plumbing.fitting import Fitting
from ocelot.pipeline.plumbing.pipeline import Pipeline
from ocelot.tests import TestCase


class FakeChannel(object):
    def process(self, data):
        pass


class TestPipeline(TestCase):
    def test_name_stored(self):
        """Test that the pipeline name is stored on the pipeline."""
        p = Pipeline('fake_name')

        self.assertEquals(
            p.name,
            'fake_name',
        )

    def test_input_fittings(self):
        """Test that only input fittings (no sources) are returned."""
        fake_channel = FakeChannel()
        fake_connected_channel = FakeChannel()

        p = Pipeline('fake_name')
        channel_fitting = p.add_channel(fake_channel)
        connected_channel_fitting = p.add_channel(fake_connected_channel)

        # Connect fake_channel -> fake_connected_channel
        channel_fitting.connect_fitting(connected_channel_fitting)

        # Only the fake_channel should be an input fitting
        self.assertEquals(len(p.fittings), 2)
        self.assertEquals(len(p.input_fittings), 1)
        self.assertEquals(p.input_fittings[0], channel_fitting)

    def test_add_channel(self):
        """Test that a new Fitting is returned and added to the fittings."""
        p = Pipeline('fake_name')

        self.assertEquals(len(p.fittings), 0)

        fitting = p.add_channel(FakeChannel())
        self.assertIsInstance(fitting, Fitting)
        self.assertEquals(len(p.fittings), 1)

    def test_run(self):
        """Test that process is called on all input fittings."""
        p = Pipeline('fake_name')

        self.assertEquals(len(p.fittings), 0)

        fitting = p.add_channel(FakeChannel())

        with mock.patch.object(fitting, 'process') as mock_process:
            p.run('fake_data')

        mock_process.assert_called_once_with('fake_data')
