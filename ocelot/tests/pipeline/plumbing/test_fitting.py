import mock

from ocelot.pipeline.exceptions import StopProcessingException
from ocelot.pipeline.plumbing.fitting import Fitting
from ocelot.pipeline.plumbing.pipe import Pipe
from ocelot.tests import TestCase


class FakeTask(object):
    @property
    def is_input(self):
        return False

    def process(self, data):
        pass


class TestFitting(TestCase):
    def test_identifier_saved(self):
        """Test that a supplied identifier is saved."""
        fitting = Fitting(
            FakeTask(),
            identifier='fake_identifier',
        )

        self.assertEquals(
            fitting.identifier,
            'fake_identifier',
        )

    def test_unique_identifier_generated(self):
        """Test that a unique identifier is generated if not provided."""
        fitting1 = Fitting(
            FakeTask(),
        )

        fitting2 = Fitting(
            FakeTask()
        )

        self.assertIsNotNone(fitting1.identifier)
        self.assertIsNotNone(fitting2.identifier)
        self.assertNotEquals(fitting1.identifier, fitting2.identifier)

    def test_is_input_true(self):
        """Test that is_input returns True when a task is an input."""

        with mock.patch.object(
            FakeTask,
            'is_input',
            new_callable=mock.PropertyMock,
        ) as mock_is_input:
            mock_is_input.return_value = True

            fitting = Fitting(FakeTask())
            self.assertTrue(fitting.is_input)

    def test_is_input_false(self):
        """Test that is_input returns False when a task is not an input."""
        with mock.patch.object(
            FakeTask,
            'is_input',
            new_callable=mock.PropertyMock,
        ) as mock_is_input:
            mock_is_input.return_value = False

            fitting = Fitting(FakeTask())
            self.assertFalse(fitting.is_input)

    def test_output_pipes(self):
        """Test that only output pipes are returned."""
        fitting = Fitting(FakeTask())
        fitting2 = Fitting(FakeTask())
        fitting3 = Fitting(FakeTask())

        fitting.connect_fitting(fitting2)
        fitting3.connect_fitting(fitting)

        self.assertEquals(len(fitting.output_pipes), 1)
        self.assertTrue(fitting.output_pipes[0].is_input(fitting))

    def test_source_pipes(self):
        """Test that only source pipes are returned."""
        fitting = Fitting(FakeTask())
        fitting2 = Fitting(FakeTask())
        fitting3 = Fitting(FakeTask())

        fitting.connect_fitting(fitting2)
        fitting3.connect_fitting(fitting)

        self.assertEquals(len(fitting.source_pipes), 1)
        self.assertTrue(fitting.source_pipes[0].is_output(fitting))

    def test_add_pipe(self):
        """Test that a pipe is added to the pipes."""
        fitting = Fitting(FakeTask())
        fitting2 = Fitting(FakeTask())

        self.assertEquals(len(fitting.pipes), 0)
        fitting.add_pipe(Pipe(fitting, fitting2))
        self.assertEquals(len(fitting.pipes), 1)

    def test_connect_fitting(self):
        """Test that a pipe was added to both fittings."""
        fitting = Fitting(FakeTask())
        fitting2 = Fitting(FakeTask())

        self.assertEquals(len(fitting.pipes), 0)
        self.assertEquals(len(fitting.source_pipes), 0)
        self.assertEquals(len(fitting.output_pipes), 0)

        self.assertEquals(len(fitting2.pipes), 0)
        self.assertEquals(len(fitting2.source_pipes), 0)
        self.assertEquals(len(fitting2.output_pipes), 0)

        fitting.connect_fitting(fitting2)

        self.assertEquals(len(fitting.pipes), 1)
        self.assertEquals(len(fitting.source_pipes), 0)
        self.assertEquals(len(fitting.output_pipes), 1)

        self.assertEquals(len(fitting2.pipes), 1)
        self.assertEquals(len(fitting2.source_pipes), 1)
        self.assertEquals(len(fitting2.output_pipes), 0)

    @mock.patch('ocelot.pipeline.plumbing.pipe.Pipe.process')
    @mock.patch.object(FakeTask, 'process')
    def test_process(self, mock_process, mock_pipe_process):
        """Test that the task processes the data and is passed to the
        output pipes."""
        mock_process.return_value = 'fake_response'

        fitting = Fitting(FakeTask())
        fitting2 = Fitting(FakeTask())
        fitting3 = Fitting(FakeTask())

        fitting.connect_fitting(fitting2)
        fitting.connect_fitting(fitting3)

        fitting.process('fake_data')
        mock_process.assert_called_once_with('fake_data')

        self.assertEquals(mock_pipe_process.call_count, len(fitting.output_pipes))
        mock_pipe_process.assert_called_with('fake_response')

    @mock.patch('ocelot.pipeline.plumbing.pipe.Pipe.process')
    def test_process_catches_stop_processing_error(self, mock_process):
        mock_process.side_effect = StopProcessingException

        fitting = Fitting(FakeTask())
        fitting2 = Fitting(FakeTask())

        fitting.connect_fitting(fitting2)

        # an exception should not be raised
        fitting.process('fake_data')
