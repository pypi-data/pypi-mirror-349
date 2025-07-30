.. _Untis:

Importing data from Untis
=========================

Untis is a proprietary timetable management software which is popular
in the German-speaking area, but used internationally. We provide some
import templates for importing basic data from Untis to *Core*, *Cursus*,
and *Lesrooster*:

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Untis Filename
     - Name in Untis
     - App
     - Model
   * - ``GPU001.txt``
     - Stundenplan (Timetable)
     - Lesrooster
     - Lesson/LessonBundle
   * - ``GPU002.txt``
     - Unterricht (Courses with quotas)
     - Cursus
     - Course/CourseBundle
   * - ``GPU003.txt``
     - Klassen (Classes)
     - Core
     - Group
   * - ``GPU004.txt``
     - Lehrer (Teachers)
     - Core
     - Person
   * - ``GPU005.txt``
     - Räume (Rooms)
     - Core
     - Room
   * - ``GPU006.txt``
     - Fächer (Subjects)
     - Cursus
     - Subject

.. warning::

    To ensure a correct import, all imported objects should have both a short name and a long name,
    for teachers a first and a last name.

How to export from Untis and import in AlekSIS
----------------------------------------------

1. Open Untis
2. Click on *File* in the top navbar
3. Select *Import/Export* and then *Export TXT Datei (CSV,DIF)*

   .. image:: untis_export.png
      :width: 800
      :alt: Untis import/export dialog

4. Select the file you want to export (see above for options)
5. When asked for export settings, please select *Komma* as *Trennzeichen*
   and ``"`` as *Textbegrenzung*. Please ensure that `Enconding: UTF-8` is checked.

   .. image:: untis_export_settings.png
      :width: 400
      :alt: Untis export settings dialog

To do a full import, you should use the following order:

1. Manually create time grid with slots in AlekSIS (There is no export option for this in Untis.)
2. Import the files in the following order:

   1. ``GPU005.txt``: Räume (Rooms)
   2. ``GPU006.txt``: Fächer (Subjects)
   3. ``GPU004.txt``: Lehrer (Teachers)
   4. ``GPU003.txt``: Klassen (Classes)
   5. ``GPU002.txt``: Unterricht (Courses with quotas)

Then go to *Lesson Planning → Validity Ranges* and click the *Import data* button next to the validity range you want to import data for.
Use that to import the following file:

   6. ``GPU001.txt``: Stundenplan (Timetable)
