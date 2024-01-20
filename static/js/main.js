$(document).ready(function() {
    const video = document.getElementById('kamera');
    const canvas = document.getElementById('tuval');
    const kameraBaslatButonu = document.getElementById('kamerayi-baslat');
    const fotografCekButonu = document.getElementById('fotograf-cek');

    $('#resim').change(function(e) {
        const dosya = e.target.files[0];
        const okuyucu = new FileReader();
        okuyucu.onload = function(e) {
            $('#orijinal').attr('src', e.target.result);
        };
        okuyucu.readAsDataURL(dosya);
    });

    $('#islemFormu').submit(function(e) {
    e.preventDefault();

    const formVerisi = new FormData(this);

    $.ajax({
        url: '/process_image',
        type: 'POST',
        data: formVerisi,
        processData: false,
        contentType: false,
        success: function(response) {
            if (response.status === 'success') {
                $('#sonuc').attr('src', response.image);
            } else {
                alert('Hata: ' + response.message);
            }
        },
        error: function() {
            alert('Resim işlenirken bir hata oluştu.');
        }
    });
});

    kameraBaslatButonu.addEventListener('click', async function() {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        video.play();
    });

    const kameraDurdurButonu = document.getElementById('kamerayi-durdur');
    let kameraAkisi = null;

    kameraBaslatButonu.addEventListener('click', async function() {
        kameraAkisi = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = kameraAkisi;
        video.play();
    });

    kameraDurdurButonu.addEventListener('click', function() {
        if (kameraAkisi) {
            const izler = kameraAkisi.getTracks();
            izler.forEach(iz => iz.stop());
            video.srcObject = null;
            kameraAkisi = null;
        }
    });

    fotografCekButonu.addEventListener('click', function() {
        const context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const veriUrl = canvas.toDataURL('image/png');
        $('#orijinal').attr('src', veriUrl);

        const blob = dataURLToBlob(veriUrl);
        const dosya = new File([blob], 'cekilen_resim.png', { type: 'image/png' });
        const veriTransfer = new DataTransfer();
        veriTransfer.items.add(dosya);
        document.getElementById('resim').files = veriTransfer.files;
    });

    function dataURLToBlob(dataURL) {
        const parcalar = dataURL.split(';base64,');
        const byteString = atob(parcalar[1]);
        const mimeString = parcalar[0].split(':')[1];
        const ab = new ArrayBuffer(byteString.length);
        const ia = new Uint8Array(ab);
        for (let i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i);
        }
        return new Blob([ab], { type: mimeString });
    }
});