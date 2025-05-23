<script type="module" lang="js">
function addManualTriangle(){
  const faces = document.getElementById('faces');
  const coords = document.getElementById('coords');
  const colors = document.getElementById('colors');

  if (!faces || !coords || !colors) {
    console.error('X3D elements not found');
    return;
  }  

  const p1 = {
    x: parseFloat(document.getElementById('p1x').value),
    y: parseFloat(document.getElementById('p1y').value),
    z: parseFloat(document.getElementById('p1z').value)
  };
  const p2 = {
    x: parseFloat(document.getElementById('p2x').value),
    y: parseFloat(document.getElementById('p2y').value),
    z: parseFloat(document.getElementById('p2z').value)
  };
  const p3 = {
    x: parseFloat(document.getElementById('p3x').value),
    y: parseFloat(document.getElementById('p3y').value),
    z: parseFloat(document.getElementById('p3z').value)
  };
  // check if all points are valid
  if (isNaN(p1.x) || isNaN(p1.y) || isNaN(p1.z) ||
      isNaN(p2.x) || isNaN(p2.y) || isNaN(p2.z) ||
      isNaN(p3.x) || isNaN(p3.y) || isNaN(p3.z)) {
    return;
  }

  addTriangle(faces, coords, colors, p1, p2, p3);
}

function reset() {
  let scene = document.getElementById('x3dScene');
  const content = "<transform translation='0 0 0'><Shape><IndexedFaceSet id=\"faces\" solid='false' coordIndex='-1'><Coordinate id=\"coords\" point=''/><Color id=\"colors\" color=''/></IndexedFaceSet></Shape></transform>";
  scene.innerHTML = content;
}


function getBox(x, y, z){
  return "<Shape><Box size='"+ x + " "+ y + " " + z +"' /></Shape>";
}

function getSphere(r){
  return "<Shape><Sphere radius='"+ r +"' /></Shape>";
}

function getCylinder(r, h){
  return "<Shape><Cylinder radius='"+r+"' height='"+h+"' /></Shape>";

}

function getCone(r_b, h, r_t){
  return "<Shape><Cone bottomRadius='"+r_b+"' topRadius='"+r_t+"' height='"+h+"' /></Shape>";
}

function translate(x, y, z, obj){
  return "<transform translation='"+ x + " "+ y + " " + z +"'>" + obj + "</transform>";
}
function rotate(x, y, z, obj){
  x  = x / 360 * 2 * Math.PI; // convert degrees to radians
  y  = y / 360 * 2 * Math.PI; // convert degrees to radians
  z  = z / 360 * 2 * Math.PI; // convert degrees to radians

  if( x === 0 && y === 0 && z === 0) {
    return obj; // no rotation
  }
  // normalize the vector (x, y, z) 
  const length = Math.sqrt(x * x + y * y + z * z);
  
  x /= length;
  y /= length;
  z /= length;

  return "<transform rotation='"+ x + " "+ y + " " + z +" " + length + "'>" + obj + "</transform>";
}

function generateCity() {
  let scene = document.getElementById('x3dScene');
  if (!scene) {
    console.error('X3D scene not found');
    return;
  }
  const width = parseFloat(document.getElementById('width').value);
  const scale = parseFloat(document.getElementById('scale').value);

  // check if all points are valid
  if (isNaN(width) || isNaN(scale)) {
    console.error('Invalid width or scale');
    return;
  }
  scene.innerHTML = generateCityContent(width, width, scale);
  scene.innerHTML += rotate(0, 90, 0 , generateCityContent(width, width, scale));
  scene.innerHTML += rotate(0, 180, 0 , generateCityContent(width, width, scale));
  scene.innerHTML += rotate(0, 270, 0 , generateCityContent(width, width, scale));
}

function generateCityContent(width, length, scale) {
  let content = "";
  // create a city out of boxes
  for (let x = 0; x < width; x++) {
    for (let z = 0; z < length; z++) {
      // random height between 1 and 10
      let h = Math.floor(Math.random() * 10) + 1;
      // random width and length between 1 and 5
      let w = Math.floor(Math.random() * scale) + 1;
      let l = Math.floor(Math.random() * scale) + 1;
      content += translate(x * w, h / 2, z * l, getBox(w, h, l));
    }
  }
  return content;
}

function addPoint(coords, colors, p) {
  let index = -1;
  const points = coords.getAttribute("point");
  // space separated string to array
  const pointsArray = points.split(" ");
  // iterate over three points at a time
  for (let i = 0; i < pointsArray.length - 1; i += 3) {
    const x = parseFloat(pointsArray[i]);
    const y = parseFloat(pointsArray[i + 1]);
    const z = parseFloat(pointsArray[i + 2]);
    if (x === p.x && y === p.y && z === p.z) {
      return i / 3;
    }
  }
  // if point not found, add it to the array
  pointsArray.push(p.x.toString(), p.y.toString(), p.z.toString());
  //array to space string
  coords.setAttribute("point", pointsArray.join(" ").trim());
  colors.setAttribute("color", (colors.getAttribute("color") + ` ${0} ${0} ${0}`).trim());
  index = Math.floor(pointsArray.length / 3) - 1;

  return index;
}
function addTriangle(faces, coords, colors, p1 , p2 , p3) {
  let i1 = addPoint(coords, colors, p1);
  let i2 = addPoint(coords, colors, p2);
  let i3 = addPoint(coords, colors, p3);
  let coordIndexes = faces.getAttribute("coordIndex");
  faces.setAttribute("coordIndex", coordIndexes.replace("-1", `${i1} ${i2} ${i3} -1`));
}


function addPoint_mapped(coords, colors, p, mapping) {
  let index = mapping.get(p);
  if(index !== undefined) {
    return index;
  }

  index = mapping.size;
  mapping.set(p, index);
  //array to space string
  coords.setAttribute("point", (coords.getAttribute("point") + ` ${p.x.toString()} ${p.y.toString()} ${p.z.toString()}`).trim());
  colors.setAttribute("color", (colors.getAttribute("color") + ` ${0} ${0} ${0}`).trim());

  return index;
}
function addTriangle_mapped(faces, coords, colors, p1 , p2 , p3, mapping) {
  let i1 = addPoint_mapped(coords, colors, p1, mapping);
  let i2 = addPoint_mapped(coords, colors, p2, mapping);
  let i3 = addPoint_mapped(coords, colors, p3, mapping);
  let coordIndexes = faces.getAttribute("coordIndex");
  faces.setAttribute("coordIndex", coordIndexes.replace("-1", `${i1} ${i2} ${i3} -1`));
}
</script>

<script setup lang="js">
document.addEventListener('DOMContentLoaded', () => {
  const dropArea = document.getElementById('drop-area');
  const fileInput = document.getElementById('file-input');

  if (!dropArea || !fileInput) {
    console.error('Drop area or file input not found');
    return;
  }
  fileInput.addEventListener('change', async () => {
    if (!fileInput || !fileInput.files) {
      console.error('File input not found');
      return;
    }
    const faces = document.getElementById('faces');
    const coords = document.getElementById('coords');
    const colors = document.getElementById('colors');

    // simple html elemnet
    let fakeFaces = document.createElement('div');
    fakeFaces.setAttribute('coordIndex', '-1');
    let fakeCoords = document.createElement('div');
    fakeCoords.setAttribute('point', '');
    let fakeColors = document.createElement('div');
    fakeColors.setAttribute('color', '');
    // read file line by line
    const file = fileInput.files[0];
    const reader = new FileReader();
    reader.onload = async (event) => {
      const mapped = new Map();
      const lines = event.target.result.split('\n');
      let p1, p2, p3;
      for (const line of lines) {
        let parts = line.trim().split(' ');
        parts = parts.filter(part => part !== ''); // remove empty strings
        if (parts[0] === 'v') {
          if (p1 === undefined) {
            p1 = { x: parseFloat(parts[1]), y: parseFloat(parts[2]), z: parseFloat(parts[3]) };
          } else if (p2 === undefined) {
            p2 = { x: parseFloat(parts[1]), y: parseFloat(parts[2]), z: parseFloat(parts[3]) };
          } else if (p3 === undefined) {
            p3 = { x: parseFloat(parts[1]), y: parseFloat(parts[2]), z: parseFloat(parts[3]) };
            addTriangle_mapped(fakeFaces, fakeCoords, fakeColors, p1, p2, p3, mapped);
            p1 = undefined;
            p2 = undefined;
            p3 = undefined;
          }
        }
        const progress = Math.floor((lines.indexOf(line) / lines.length) * 100);
        console.log(`Progress: ${progress}%`);
      }
      // set the attributes to the x3d elements
      coords.setAttribute('point', fakeCoords.getAttribute('point'));
      colors.setAttribute('color', fakeColors.getAttribute('color'));
      faces.setAttribute('coordIndex', fakeFaces.getAttribute('coordIndex'));
    };
    reader.readAsText(file);

  });
  dropArea.addEventListener('click', () => fileInput.click());

  dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropArea.classList.add('bg-gray-200');
  });

  dropArea.addEventListener('dragleave', () => {
    dropArea.classList.remove('bg-gray-200');
  });

  dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropArea.classList.remove('bg-gray-200');
    if (e.dataTransfer?.files.length) {
      fileInput.files = e.dataTransfer.files;
      // Handle the file as needed
    }
  });
});

</script>


<template>
  <div id="container" class="min-w-1/4">
    <div id="controls">
      <h1>G3D Ass4</h1>
    </div>
    <div id="drop-area"
         class="border-2 mt-4 border-dashed border-gray-400 rounded-lg p-8 text-center cursor-pointer transition hover:bg-gray-100 ">
      <p>Drag & drop a .obj file here, or <span class="text-blue-600 underline">click to
            select</span>
      </p>
      <input type="file" id="file-input" accept=".obj" class="hidden" />
    </div>
    <div class="my-4 p-4 border rounded ">
      <div class="mb-2 font-semibold">Add Triangle (manual):</div>
      <div class="flex flex-col gap-2">
        <div class="flex gap-2 items-center">
          <span>P1:</span>
          <input id="p1x" type="number" placeholder="x" value="0" class="flex w-1/3 border rounded px-1" />
          <input id="p1y" type="number" placeholder="y" value="0" class="flex w-1/3 border rounded px-1" />
          <input id="p1z" type="number" placeholder="z" value="0" class="flex w-1/3 border rounded px-1" />
        </div>
        <div class="flex gap-2 items-center">
          <span>P2:</span>
          <input id="p2x" type="number" placeholder="x" value="0" class="flex w-1/3 border rounded px-1" />
          <input id="p2y" type="number" placeholder="y" value="0" class="flex w-1/3 border rounded px-1" />
          <input id="p2z" type="number" placeholder="z" value="0" class="flex w-1/3 border rounded px-1" />
        </div>
        <div class="flex gap-2 items-center">
          <span>P3:</span>
          <input id="p3x" type="number" placeholder="x" value="0" class="flex w-1/3 border rounded px-1" />
          <input id="p3y" type="number" placeholder="y" value="0" class="flex w-1/3 border rounded px-1" />
          <input id="p3z" type="number" placeholder="z" value="0" class="flex w-1/3 border rounded px-1" />
        </div>
        <button @click="addManualTriangle"
                class="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
          Add Triangle
        </button>
      </div>
    </div>
    <div class="my-4 p-4 border rounded ">
      <div class="mb-2 font-semibold">Generate City:</div>
      <div class="flex flex-col gap-2">
        <div class="flex gap-2 items-center">
          <span class="flex w-1/6">Width:</span>
          <input id="width" type="number" placeholder="Width" value="10" class="flex w-1/3 border rounded px-1" />
          <span class="flex w-1/6">Scale:</span>
          <input id="scale" type="number" placeholder="Scale" value="3" class="flex w-1/3 border rounded px-1" />
        </div>
        <button @click="generateCity"
                class="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
          Generate City
        </button>
    </div>
    </div>
    <div class="my-4 p-4 border rounded ">
      
        <div class="flex flex-col gap-2"><button @click="reset"
              class="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition">
        Reset
      </button></div>
      
    </div>
</div>
</template>
