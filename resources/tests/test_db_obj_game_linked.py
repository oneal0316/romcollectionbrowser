import unittest
import os
import sys
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'lib'))

from gamedatabase import GameDataBase, Genre, Year, Publisher, Developer


class TestDBObjGame(unittest.TestCase):
    ''' Test the objects linked to the Game DB row by ID
    '''
    gdb = None

    @classmethod
    def get_testdata_path(cls):
        return os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'tests', 'testdata')

    @classmethod
    def setUpClass(cls):
        # Open the DB
        db_path = os.path.join(cls.get_testdata_path(), 'database')

        # Setup data - MyGames.db is the hard-coded expected DB name
        shutil.copyfile(os.path.join(db_path, 'test.db'), os.path.join(db_path, 'MyGames.db'))

        cls.gdb = GameDataBase(db_path)
        cls.gdb.connect()

    @classmethod
    def tearDownClass(cls):
        # Cleanup
        cls.gdb.close()
        os.remove(os.path.join(os.path.join(cls.get_testdata_path(), 'database'), 'MyGames.db'))

    ''' Genres '''

    def test_RetrieveSingleGenreByGameId(self):
        ''' Validate basic retrieve works '''
        genre = Genre(self.gdb).getGenresForGame(28)

        self.assertTrue(genre == 'Role-Playing', 'Genre for game id 28 expected to be Role-Playing')

    def test_RetrieveMultipleGenresByGameId(self):
        ''' Test that games with multiple genres are comma-separated strings FIXME TODO Order of genres '''
        genres = Genre(self.gdb).getGenresForGame(50)
        print genres

        self.assertTrue(genres == 'Adventure, Action, Role-Playing', 'Expected multiple genres for game to be comma-separated string, was {0}'.format(genres))

    def test_RetrieveGameWithSlash(self):
        ''' Validate items with genre e.g. Action/Adventure are handled '''
        genres = Genre(self.gdb).getGenresForGame(179)

        self.assertTrue(genres == 'Racing / Driving, Role-Playing (RPG)', 'Game with slash in genre not handled correctly (was {0})'.format(genres))

    ''' Developer '''
    def test_RetrieveDeveloperByGameId(self):
        ''' Validate basic retrieve works '''
        dev = Developer(self.gdb).getDeveloperForGame(62)

        self.assertTrue(dev == 'Squaresoft', 'Expected developer for game with id 62 to be Squaresoft, was {0}'.format(dev))

    def test_RetrieveDeveloper(self):
        dev = Developer(self.gdb).getDeveloper(2)
        self.assertTrue(dev == 'Activision')

    ''' Publisher '''
    def test_RetrievePublisherByGameId(self):
        ''' Validate basic retrieve works '''
        pub = Publisher(self.gdb).getPublisherForGame(6)

        self.assertTrue(pub == 'Stern', 'Expected publisher for game with id 6 to be Stern, was {0}'.format(pub))

    def test_RetrievePublisher(self):
        pub = Publisher(self.gdb).getPublisher(6)
        self.assertTrue(pub == 'Nintendo')

if __name__ == "__main__":
    unittest.main()
