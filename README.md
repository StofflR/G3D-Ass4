# WebApp

A web app version of the application can be found under https://stofflr.github.io/G3D-Ass4/ hosted via GitHub Pages.

## Requirements
To run the app yarn is required. See https://yarnpkg.com/getting-started/install on how to install yarn.

## Setup § Building
Run `yarn` to install all package dependencies.
Executing `yarn run dev` will launch the application in development mode. The application will be available via localhost.

## Building and running

### Web app
Executing `yarn run build` will create the application in the _.\dist_.
The web application is now 'portable' and the contents of the _.\dist_ folder can be moved to the desired directory.
To run the application a HTTP Server is required. For testing purposes `python3 -m http.server` could be used.

### Functionality

#### IndexedFaceSet
The indexed face set is implemented in _.\app\src\components\Chart.vue_. Adding triangles to it via `addTriangle` will add a triangle to the indexed face set. The triangles are defined by three points, which are defined by their x, y and z coordinates.
```
<IndexedFaceSet id="faces" solid='false' coordIndex='-1'>
    <Coordinate id="coords" point=''/>
    <Color id="colors" color=''/>
</IndexedFaceSet>
```
The fields `coordIndex` and `point` are used to define the triangles. The `coordIndex` is a list of indices that point to the coordinates in the `point` field. The `point` field is a list of coordinates that define the points of the triangles. The `colors` field could be used to define the colors of the triangles.

For inizialization the `coordIndex` and `point` fields are set to empty strings. On loading the page they are inizialised with the indexed face set data of _.\app\assets\vertices.txt_, _.\app\assets\faces.txt_ and _.\app\assets\colors.txt_.

#### Loading obj files
The app can load object files, although this is rather slow as it is not implemented in a very efficient way.

