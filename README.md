# Profile Editor Web App

A simple web application to update and manage your professional profile information stored in `profile.json`.

## Features

- Edit basic information (name, title, summary)
- Update contact details (email, phone, location, social links)
- Manage skills with categories
- Add, edit, and remove work experience entries
- Responsive design that works on desktop and mobile
- Real-time preview of changes
- Data validation and error handling

## Prerequisites

- A web server with PHP support (for saving changes)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Installation

1. Upload all files to your web server
2. Ensure the web server has write permissions for the directory containing `profile.json`
3. Open `update-profile.html` in your web browser

## Usage

1. **Basic Information**: Update your name, professional title, and summary.
2. **Contact Information**: Keep your contact details up to date.
3. **Skills**: 
   - Add new skill categories
   - Edit existing skills
   - Remove categories you no longer need
4. **Experience**:
   - Add new work experience entries
   - Edit job titles, companies, and descriptions
   - Update technologies used
   - Remove outdated positions
5. **Saving Changes**:
   - Click "Save Changes" to update your profile
   - The original `profile.json` will be backed up automatically
   - Use "Reset" to discard changes and reload the original data

## Security Notes

- The application makes AJAX requests to `save-profile.php`
- The PHP script creates backups before saving changes
- Ensure proper file permissions are set on your web server
- For production use, consider adding authentication

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is open source and available under the [MIT License](LICENSE).
