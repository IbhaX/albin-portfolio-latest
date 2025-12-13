// TinyMCE initialization for Django Admin
document.addEventListener('DOMContentLoaded', function() {
    // Selectors for textarea fields that should have WYSIWYG
    const wysiwygFields = [
        'id_content',
        'id_description', 
        'id_owner_summary',
        'id_achievements',
        'id_excerpt',
        'id_bio'
    ];
    
    wysiwygFields.forEach(fieldId => {
        const el = document.getElementById(fieldId);
        if (el && el.tagName === 'TEXTAREA') {
            tinymce.init({
                selector: '#' + fieldId,
                plugins: 'anchor autolink charmap codesample emoticons image link lists media searchreplace table visualblocks wordcount code',
                toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table | align lineheight | numlist bullist indent outdent | emoticons charmap | removeformat | code',
                height: 400,
                menubar: true,
                branding: false,
                promotion: false,
                skin: 'oxide-dark',
                content_css: 'dark',
                setup: function(editor) {
                    editor.on('change', function() {
                        editor.save();
                    });
                }
            });
        }
    });
});
