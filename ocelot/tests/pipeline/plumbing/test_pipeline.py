import mock

from ocelot.pipeline.tasks.base_task import BaseTask
from ocelot.pipeline.tasks.inputs.base_input import BaseInput
from ocelot.pipeline.plumbing.fitting import Fitting
from ocelot.pipeline.plumbing.pipeline import Pipeline
from ocelot.tests import TestCase


class FakeTask(BaseTask):
    def process(self, data):
        pass


class FakeInputTask(BaseInput):
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
        fake_task = FakeInputTask()
        fake_connected_task = FakeTask()

        p = Pipeline('fake_name')
        task_fitting = p.add_task(fake_task)
        connected_task_fitting = p.add_task(fake_connected_task)

        # Connect fake_task -> fake_connected_task
        task_fitting.connect_fitting(connected_task_fitting)

        # Only the fake_task should be an input fitting
        self.assertEquals(len(p.fittings), 2)
        self.assertEquals(len(p.input_fittings), 1)
        self.assertEquals(p.input_fittings[0], task_fitting)

    def test_add_task(self):
        """Test that a new Fitting is returned and added to the fittings."""
        p = Pipeline('fake_name')

        self.assertEquals(len(p.fittings), 0)

        fitting = p.add_task(FakeInputTask())
        self.assertIsInstance(fitting, Fitting)
        self.assertEquals(len(p.fittings), 1)

    def test_run(self):
        """Test that process is called on all input fittings."""
        p = Pipeline('fake_name')

        self.assertEquals(len(p.fittings), 0)

        fitting = p.add_task(FakeInputTask())

        with mock.patch.object(fitting, 'process') as mock_process:
            p.run('fake_data')

        mock_process.assert_called_once_with('fake_data')
