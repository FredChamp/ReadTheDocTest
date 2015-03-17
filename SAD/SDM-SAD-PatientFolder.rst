    DICOM is a software integration standard that is used in Medical Imaging. All modern medical imaging systems (aka Imaging Modalities) equipment like X-Rays,
    Ultrasounds, CT (Computed Tomography), and MRI (Magnetic Resonance Imaging) support DICOM and use it extensively. The core of DICOM is a file format and a networking protocol.

    All Medical Images are saved in DICOM format. Medical Imaging Equipment creates DICOM files. Doctors use DICOM Viewers, computer software applications that can display DICOM images.

    DICOM files contain more than just images. Every DICOM file holds patient information (name, ID, sex and birth date), important acquisition data (e.g., type of equipment used and its settings), and the context of the imaging study that is used to link the image to the medical treatment it was part of.
    
Roni Z. 2011. Introduction to DICOM [#]_:

.. [#] Roni Z. 2011. Introduction to DICOM. Introduction. http://dicomiseasy.blogspot.fr/2011/10/introduction-to-dicom-chapter-1.html

|

The objects representing the medical patient data In FW4SPL are aligned with the DICOM standard. In the library ``fwMedData`` several structures and values have been retrieved:

- ``Patient``: name, primary hospital identification number, birth date and sex.
- ``Study``: unique identifier of the study, study date and time, referring
  physician, institution-generated description, age of the patient.
- ``Equipment``: institution where the equipment that produced the composite
  instances is located.
- ``Series``: unique identifier of the series, type of equipment that
  originally acquired the data used to create this series, series date and
  time, series description, name of the physician(s) administering the series.

In FW4SPL, the class ``Series`` is the main structure and contains pointers
to Patient, Study and Equipment structure. The class ``SeriesDB`` is a
container holding several instances of the ``Series`` class.

To specify an object of type ``Series``, the library ``fwMedData`` holds the following classes inherited from ``Series``:

- ``ImageSeries`` which corresponds to the image series of DICOM (CT images, MRI images,
  etc).
- ``ModelSeries`` which corresponds to the meshes series of DICOM and also represents
  3D patient models.

The ``fwMedData`` library also provides a custom series called ``ActivitySeries``. An ``ActivitySeries`` is a ``Series`` linked to an
activity (sub part an application). Hence it is possible to save the state of all the objects used in the activity. 
Further application specific parameters which are not referred to an object can also be saved in an ``ActivitySeries``. 
Application parameters in relation to the patient can be the view point on an organ,
landmarks, calculated distances between organ points, etc.
