# coding=utf-8
import sys
import os
import shutil
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'lib', 'pyscraper'))

import xbmcaddon
from nfowriter import NfoWriter
from nfo_scraper import NFO_Scraper
from gamedatabase import GameDataBase
from config import Config, RomCollection


class Test_NFOWriter(unittest.TestCase):

    def test_getNfoFilePath(self):

        xbmcaddon._settings['rcb_nfoFolder'] = ''

        writer = NfoWriter()
        filename = writer.getNfoFilePath("Amiga", "./testdata/roms/Amiga/Airborne Ranger.adf", "Airborne Ranger")

        filename = filename.replace("\\", "/")

        self.assertEquals("./testdata/roms/Amiga/Airborne Ranger.nfo", filename)


    def test_getNfoFilePath_path_in_settings(self):

        xbmcaddon._settings['rcb_nfoFolder'] = './testdata/nfo/'

        writer = NfoWriter()
        filename = writer.getNfoFilePath("Amiga", "./testdata/roms/Amiga/Airborne Ranger.adf", "Airborne Ranger")

        filename = filename.replace("\\", "/")

        self.assertEquals("./testdata/nfo/Amiga/Airborne Ranger.nfo", filename)


    def test_createNfoFromDesc_newfile(self):
        xbmcaddon._settings['rcb_nfoFolder'] = './testdata/nfo/'

        self.assertFalse(os.path.isfile('./testdata/nfo/Amiga/Airborne Ranger.nfo'), 'nfo file should not exist')

        writer = NfoWriter()
        writer.createNfoFromDesc('Airborne Ranger', #gamename
                                 "Description with some special characters: ' & <  >", #plot
                                 'Amiga', #romCollectionname
                                 '"MicroProse"', #publisher
                                 'Imagitec', #developer
                                 '1989', #year
                                 '1', #players
                                 '3.2', #rating
                                 '128', #votes
                                 '', #url
                                 'USA', #region
                                 'Floppy', #media
                                 'Top-Down', #perspective
                                 'Joystick', #controller
                                 'Airborne Ranger', #originalTitle
                                 'Airborne Ranger', #alternateTitle
                                 'v1.00', #version
                                 ['Action', 'Simulation'], #genreList
                                 '1', #isFavorite
                                 '1', #launchCount
                                 './testdata/roms/Amiga/Airborne Ranger.adf', #romFile
                                 'Airborne Ranger', #gamenameFromFile
                                 {}, #artworkfiles
                                 {} #artworkurls
                                    )

        self.assertTrue(os.path.isfile('./testdata/nfo/Amiga/Airborne Ranger.nfo'), 'Expected nfo file to be written')

        #use nfo scraper to read the file
        scraper = NFO_Scraper()
        scraper.nfo_file = './testdata/nfo/Amiga/Airborne Ranger.nfo'

        result = scraper.retrieve(1, 'Amiga')

        self.assertEqual(["Airborne Ranger"], result['Game'])
        self.assertEqual(["Airborne Ranger"], result['OriginalTitle'])
        self.assertEqual(["Airborne Ranger"], result['AlternateTitle'])
        self.assertEqual(["1989"], result['ReleaseYear'])
        self.assertEqual(['"MicroProse"'], result['Publisher'])
        self.assertEqual(["Imagitec"], result['Developer'])
        self.assertEqual(["Top-Down"], result['Perspective'])
        self.assertEqual(["Joystick"], result['Controller'])
        self.assertEqual(["Floppy"], result['Media'])
        self.assertEqual(["USA"], result['Region'])
        self.assertEqual(["v1.00"], result['Version'])
        self.assertEqual(["1"], result['Players'])
        self.assertEqual(["1"], result['LaunchCount'])
        self.assertEqual(["1"], result['IsFavorite'])
        self.assertEqual(["3.2"], result['Rating'])
        self.assertEqual(["128"], result['Votes'])
        self.assertTrue(result['Description'][0].startswith(
            "Description with some special characters: ' & <  >"))
        self.assertEqual(len(result['Genre']), 2)
        self.assertIn("Action", result['Genre'])
        self.assertIn("Simulation", result['Genre'])

        os.remove('./testdata/nfo/Amiga/Airborne Ranger.nfo')


    def test_createNfoFromDesc_newfile_missinginfos(self):
        xbmcaddon._settings['rcb_nfoFolder'] = './testdata/nfo/'

        self.assertFalse(os.path.isfile('./testdata/nfo/Amiga/Airborne Ranger.nfo'), 'nfo file should not exist')

        writer = NfoWriter()
        writer.createNfoFromDesc('Airborne Ranger', #gamename
                                 '', #plot
                                 'Amiga', #romCollectionname
                                 '', #publisher
                                 '', #developer
                                 '', #year
                                 '', #players
                                 '', #rating
                                 '', #votes
                                 '', #url
                                 '', #region
                                 '', #media
                                 '', #perspective
                                 '', #controller
                                 '', #originalTitle
                                 '', #alternateTitle
                                 '', #version
                                 [], #genreList
                                 '', #isFavorite
                                 '', #launchCount
                                 './testdata/roms/Amiga/Airborne Ranger.adf', #romFile
                                 'Airborne Ranger', #gamenameFromFile
                                 {}, #artworkfiles
                                 {} #artworkurls
                                    )

        self.assertTrue(os.path.isfile('./testdata/nfo/Amiga/Airborne Ranger.nfo'), 'Expected nfo file to be written')

        #use nfo scraper to read the file
        scraper = NFO_Scraper()
        scraper.nfo_file = './testdata/nfo/Amiga/Airborne Ranger.nfo'

        result = scraper.retrieve(1, 'Amiga')

        self.assertEqual(["Airborne Ranger"], result['Game'])
        self.assertEqual([None], result['OriginalTitle'])
        self.assertEqual([None], result['AlternateTitle'])
        self.assertEqual([None], result['ReleaseYear'])
        self.assertEqual([None], result['Publisher'])
        self.assertEqual([None], result['Developer'])
        self.assertEqual([None], result['Perspective'])
        self.assertEqual([None], result['Controller'])
        self.assertEqual([None], result['Media'])
        self.assertEqual([None], result['Region'])
        self.assertEqual([None], result['Version'])
        self.assertEqual([None], result['Players'])
        self.assertEqual([None], result['LaunchCount'])
        self.assertEqual([None], result['IsFavorite'])
        self.assertEqual([None], result['Rating'])
        self.assertEqual([None], result['Votes'])
        self.assertEqual([None], result['Description'])
        self.assertEqual(len(result['Genre']), 0)

        os.remove('./testdata/nfo/Amiga/Airborne Ranger.nfo')


    def test_createNfoFromDesc_existingfile(self):
        xbmcaddon._settings['rcb_nfoFolder'] = './testdata/nfo/'

        self.assertFalse(os.path.isfile('./testdata/nfo/Amiga/Airborne Ranger.nfo'), 'nfo file should not exist')

        shutil.copy('./testdata/nfo/Amiga/Airborne Ranger_orig.nfo', './testdata/nfo/Amiga/Airborne Ranger.nfo')

        writer = NfoWriter()
        #missing infos should be merged with infos from existing file
        writer.createNfoFromDesc('Airborne Ranger', #gamename
                                 '', #plot
                                 'Amiga', #romCollectionname
                                 '', #publisher
                                 '', #developer
                                 '', #year
                                 '', #players
                                 '', #rating
                                 '', #votes
                                 '', #url
                                 '', #region
                                 '', #media
                                 '', #perspective
                                 '', #controller
                                 'Airborne Ranger', #originalTitle
                                 'Airborne Ranger', #alternateTitle
                                 '', #version
                                 [], #genreList
                                 '', #isFavorite
                                 '', #launchCount
                                 './testdata/roms/Amiga/Airborne Ranger.adf', #romFile
                                 'Airborne Ranger', #gamenameFromFile
                                 {}, #artworkfiles
                                 {} #artworkurls
                                    )

        self.assertTrue(os.path.isfile('./testdata/nfo/Amiga/Airborne Ranger.nfo'), 'Expected nfo file to be written')

        #use nfo scraper to read the file
        scraper = NFO_Scraper()
        scraper.nfo_file = './testdata/nfo/Amiga/Airborne Ranger.nfo'

        result = scraper.retrieve(1, 'Amiga')

        self.assertEqual(["Airborne Ranger"], result['Game'])
        self.assertEqual(["Airborne Ranger"], result['OriginalTitle'])
        self.assertEqual(["Airborne Ranger"], result['AlternateTitle'])
        self.assertEqual(["1989"], result['ReleaseYear'])
        self.assertEqual(['"MicroProse"'], result['Publisher'])
        self.assertEqual(["Imagitec"], result['Developer'])
        self.assertEqual(["Top-Down"], result['Perspective'])
        self.assertEqual(["Joystick"], result['Controller'])
        self.assertEqual(["Floppy"], result['Media'])
        self.assertEqual(["USA"], result['Region'])
        self.assertEqual(["v1.00"], result['Version'])
        self.assertEqual(["1"], result['Players'])
        self.assertEqual(["1"], result['LaunchCount'])
        self.assertEqual(["1"], result['IsFavorite'])
        self.assertEqual(["3.2"], result['Rating'])
        self.assertEqual(["128"], result['Votes'])
        self.assertTrue(result['Description'][0].startswith(
            "Description with some special characters: ' & <  >"))
        self.assertEqual(len(result['Genre']), 2)
        self.assertIn("Action", result['Genre'])
        self.assertIn("Simulation", result['Genre'])

        os.remove('./testdata/nfo/Amiga/Airborne Ranger.nfo')


    def test_exportLibrary(self):

        export_base_folder = './testdata/nfo/export/'
        xbmcaddon._settings['rcb_nfoFolder'] = export_base_folder

        # Setup data - MyGames.db is the hard-coded expected DB name
        db_path = './testdata/database/'
        shutil.copyfile(os.path.join(db_path, 'MyGames_2.2.0_full.db'), os.path.join(db_path, 'MyGames.db'))
        gdb = GameDataBase(db_path)
        gdb.connect()

        # Setup config
        config_xml_file = './testdata/config/romcollections_importtests.xml'
        conf = Config(config_xml_file)
        conf.readXml()

        writer = NfoWriter()
        writer.exportLibrary(gdb, conf.romCollections)

        #check if all files have been created
        self.assertTrue(os.path.isfile(os.path.join(export_base_folder, 'Amiga/Airborne Ranger.nfo')))
        self.assertTrue(os.path.isfile(os.path.join(export_base_folder, 'Amiga/Chuck Rock.nfo')))
        self.assertTrue(os.path.isfile(os.path.join(export_base_folder, 'Amiga/Eliminator.nfo')))
        self.assertTrue(os.path.isfile(os.path.join(export_base_folder, 'Amiga/MicroProse Formula One Grand Prix.nfo')))
        self.assertTrue(os.path.isfile(os.path.join(export_base_folder, 'Atari 2600/Adventure (1980) (Atari).nfo')))
        self.assertTrue(os.path.isfile(os.path.join(export_base_folder, 'Atari 2600/Air-Sea Battle (32 in 1) (1988) (Atari) (PAL).nfo')))
        self.assertTrue(os.path.isfile(os.path.join(export_base_folder, 'Atari 2600/Asteroids (1981) (Atari) [no copyright].nfo')))
        #FIXME TODO: can't find file even if it exists
        #self.assertTrue(os.path.isfile(os.path.join(export_base_folder, 'Nintendo 64/1080° Snowboarding.nfo')))
        self.assertTrue(os.path.isfile(os.path.join(export_base_folder, 'PlayStation/Bushido Blade.nfo')))
        self.assertTrue(os.path.isfile(os.path.join(export_base_folder, 'PlayStation/Silent Hill.nfo')))
        self.assertTrue(os.path.isfile(os.path.join(export_base_folder, 'SNES/Chrono Trigger.nfo')))
        self.assertTrue(os.path.isfile(os.path.join(export_base_folder, "SNES/Madden NFL '97.nfo")))

        os.remove(os.path.join(export_base_folder, 'Amiga/Airborne Ranger.nfo'))
        os.remove(os.path.join(export_base_folder, 'Amiga/Chuck Rock.nfo'))
        os.remove(os.path.join(export_base_folder, 'Amiga/Eliminator.nfo'))
        os.remove(os.path.join(export_base_folder, 'Amiga/MicroProse Formula One Grand Prix.nfo'))
        os.remove(os.path.join(export_base_folder, 'Atari 2600/Adventure (1980) (Atari).nfo'))
        os.remove(os.path.join(export_base_folder, 'Atari 2600/Air-Sea Battle (32 in 1) (1988) (Atari) (PAL).nfo'))
        os.remove(os.path.join(export_base_folder, 'Atari 2600/Asteroids (1981) (Atari) [no copyright].nfo'))
        #FIXME TODO: can't find file even if it exists
        #os.remove(os.path.join(export_base_folder, 'Nintendo 64/1080° Snowboarding.nfo'))
        os.remove(os.path.join(export_base_folder, 'PlayStation/Bushido Blade.nfo'))
        os.remove(os.path.join(export_base_folder, 'PlayStation/Silent Hill.nfo'))
        os.remove(os.path.join(export_base_folder, 'SNES/Chrono Trigger.nfo'))
        os.remove(os.path.join(export_base_folder, "SNES/Madden NFL '97.nfo"))

        gdb.close()
        os.remove(os.path.join(db_path, 'MyGames.db'))