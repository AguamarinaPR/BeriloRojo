# Berilo Rojo
![Logo for Berilo Rojo](berilo.png)
## Repository generator for Aguamarina
Berilo Rojo 1.1 is a rewrite from scratch in Python that can run on Linux or Windows.
Berilo Rojo 1.0 was written in PHP and based on the Aptoide Server 1.4 PHP script and only ran on x86 Linux.

### Setting up Berilo Rojo
You will need the following:
- Python 3.14 (Written for Python 3.14, but Python 3.10 and newer versions should do fine)
Once you have Python installed, a recommended step is to go into the directory where you put Berilo Rojo and run:
```python -m venv berilorojoenv```
to create an isolated virtual environment for Berilo Rojo.
Once you have done this, any time you go into the directory for Berilo Rojo, you can activate it by running the following command:
- On Windows: `berilorojoenv\Scripts\activate`
- or on Linux: `source berilorojoenv/bin/activate`
This will activate the virual environment. This is so that any dependencies you install will be isolated to the specific environment.

You will need to install these dependencies, which you can do by running `pip install -r requirements.txt`
- Pillow (Written using Pillow 12.0.0)
- pyaxmlparser (Written using pyaxmlparser 0.3.31)

If you are using a virtual environment as was suggested, you can run `deactivate` whenever you are done using Berilo Rojo.
Whenever you want to run Berilo Rojo with this virtual environment, you can go back into the directory where you have set up Berilo Rojo run the "activate" command that was shown earlier.

### Running Berilo Rojo
Go into the directory where you have set up Berilo Rojo and activate the virtual environment.
After doing this, you can simply run the following command, while replacing the /directory/to/repository/ with the directory of your repository where you have put your APK files:
On Linux: `berilorojo.py /directory/to/repository/`
On Windows: `berilorojo.py C:/directory/to/repository/`
If you want to specify the mode of operation, after the directory, add one of these:
-a = Metadata files, info.xml and extras.xml (default mode)
-m = Metadata files only
-i = info.xml only
-e = extras.xml only
Example of usage:
```berilorojo.py /directory/to/repository/ -a```

### What is all this?
The `info.xml` is the main file of your repository, it contains the most important details of the apps in your repository. Without it, Aguamarina will not read your repository.

The `extras.xml` is the file in your directory that contains the descriptions of your apps, it is an optional but recommended inclusion.

During generation of the metadata files, you will be prompted for the information to add to them.
The metadata files are many individual `.xml` format files named after the package of each APK file in your repo, and they are contained in the `meta` subdirectory of your repo that contain metadata such as descriptions and categories.
The metadata files are not read by the Aguamarina client itself but are appended to the `info.xml` and `extras.xml` files while they are being generated, the two of which are actually read by aguamarina. They are an optional but recommended inclusion when generating `info.xml` but without them, generating `extras.xml` will be redundant.
To change the metadata for an app after it has already been generated, you can remove the metadata file for an app (Example: `meta/com.example.appname.xml`) and run Berilo Rojo again.

### Description metadata
Descriptions are contained within `<cmt>` tags.
### Primary categories
The primary category (`<catg>`) can be one of following categories:
- ```Games```
- ```Applications```
- ```Others```
  
The secondary category (`<catg2>`) can be on of the following, depending on the primary category:
#### Secondary categories for Games
> Arcade & Action, Brain & Puzzle, Cards & Casino, Casual, Emulators, Other
#### Secondary categories for Applications
> Comics, Communication, Entertainment, Finance, Health, Lifestyle, Multimedia, News & Weather, Productivity, Reference, Shopping, Social, Sports, Themes, Tools, Travel, Demo, Software Libraries, Other

After the metadata files are made, `info.xml` and `extras.xml` can be generated with information from the metadata files appended.

### 1.0 to 1.1 Repository Migrator
In Berilo Rojo 1.0, all the metadata was contained in the `extras.xml` and then appended to info.xml, but in Berilo Rojo 1.1 it is contained in individual metadata files, and then appended to `info.xml` and `extras.xml`. Because of this difference, I wrote `brmigrator.py`, which you most likely won't need to use, but is there to help convert a Berilo Rojo 1.0 `extras.xml` to Berilo Rojo 1.1 metadata xml files.
