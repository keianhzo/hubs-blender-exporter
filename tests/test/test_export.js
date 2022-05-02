const fs = require('fs');
const path = require('path');

const OUT_PREFIX = process.env.OUT_PREFIX || '../tests_out';

process.env['BLENDER_USER_SCRIPTS'] = '..';

const blenderVersions = (() => {
  if (process.platform == 'darwin') {
    return [
      "/Applications/Blender.app/Contents/MacOS/Blender"
    ];
  }
  else if (process.platform == 'linux') {
    return [
      "blender"
    ];
  }
})();

var utils = require('./utils.js').utils;

var assert = require('assert');

describe('Exporter', function () {
  let blenderSampleScenes = fs.readdirSync('scenes').filter(f => f.endsWith('.blend')).map(f => f.substring(0, f.length - 6));

  blenderVersions.forEach(function (blenderVersion) {
    let variants = [
      ['', ''],
      ['_glb', '--glb']
    ];

    variants.forEach(function (variant) {
      const args = variant[1];
      describe(blenderVersion + '_export' + variant[0], function () {
        blenderSampleScenes.forEach((scene) => {
          it(scene, function (done) {
            let outDirName = 'out' + blenderVersion + variant[0];
            let blenderPath = `scenes/${scene}.blend`;
            let ext = args.indexOf('--glb') === -1 ? '.gltf' : '.glb';
            let outDirPath = path.resolve(OUT_PREFIX, 'scenes', outDirName);
            let dstPath = path.resolve(outDirPath, `${scene}${ext}`);
            utils.blenderFileToGltf(blenderVersion, blenderPath, outDirPath, (error) => {
              if (error)
                return done(error);

              utils.validateGltf(dstPath, done);
            }, args);
          });
        });
      });
    });

    describe(blenderVersion + '_export_results', function () {
      let outDirName = 'out' + blenderVersion;
      let outDirPath = path.resolve(OUT_PREFIX, 'scenes', outDirName);

      it('can export link', function () {
        let gltfPath = path.resolve(outDirPath, 'link.gltf');
        const asset = JSON.parse(fs.readFileSync(gltfPath));

        assert.strictEqual(asset.extensionsUsed.includes('MOZ_hubs_components'), true);
        assert.strictEqual(utils.checkExtensionAdded(asset), true);

        const link = asset.nodes[0];
        assert.strictEqual(utils.checkExtensionAdded(link), true);

        const link_ext = link.extensions['MOZ_hubs_components'];
        assert.strictEqual(link_ext['link']['href'], 'https://hubs.mozilla.com');
        assert.strictEqual(utils.UUID_REGEX.test(link_ext['networked']['id']), true);
      });

      it('can export link', function () {
        let gltfPath = path.resolve(outDirPath, 'visible.gltf');
        const asset = JSON.parse(fs.readFileSync(gltfPath));

        assert.strictEqual(asset.extensionsUsed.includes('MOZ_hubs_components'), true);
        assert.strictEqual(utils.checkExtensionAdded(asset), true);

        const node = asset.nodes[0];
        assert.strictEqual(utils.checkExtensionAdded(node), true);

        const ext = node.extensions['MOZ_hubs_components'];
        assert.strictEqual(ext['visible']['visible'], true);
      });
    });
  });
});