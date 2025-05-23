<script setup lang="js">
document.addEventListener('DOMContentLoaded', () => {
  const faces = document.getElementById("faces");
  const coords = document.getElementById("coords");
  const colors = document.getElementById("colors");

  if (!faces || !coords || !colors) {
    console.error("X3D elements not found");
    return;
  }
  // Set the initial values for the IndexedFaceSet
  fetch("./app/assets/colors.txt")
    .then((res) => res.text())
    .then((text) => {
        colors.setAttribute("color", text);
      })
  .catch((e) => console.error(e));

  fetch("./app/assets/vertices.txt")
    .then((res) => res.text())
    .then((text) => {
        coords.setAttribute("point", text);
      })
  .catch((e) => console.error(e));
  
  fetch("./app/assets/indices.txt")
    .then((res) => res.text())
    .then((text) => {
        faces.setAttribute("coordIndex", text);
      })

});
</script>


<template>
  <div class="w-full">
    <div id="x3dContext-card" class="justify-center w-full">
      <x3d id="x3dContext" class="justify-center mt-2 w-full aspect-video">
        <scene id="x3dScene">
          <transform translation='0 0 0'>
            <Shape>
              <IndexedFaceSet id="faces" solid='false' coordIndex='-1'>
                <Coordinate id="coords" point=''/>
                <Color id="colors" color=''/>
              </IndexedFaceSet>
            </Shape>
          </transform>
        </scene>
      </x3d>
    </div>
  </div>
</template>
