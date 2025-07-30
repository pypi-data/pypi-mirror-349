import { useState } from 'react';
import {
  getAPIPathRoot,
  sendFetchRequest,
  removeLastSegmentFromPath
} from '../utils';
import { useFileBrowserContext } from '../contexts/FileBrowserContext';
import { useZoneBrowserContext } from '../contexts/ZoneBrowserContext';
import { useCookiesContext } from '../contexts/CookiesContext';

export default function useRenameDialog() {
  const [newName, setNewName] = useState<string>('');
  const [showAlert, setShowAlert] = useState<boolean>(false);
  const [alertContent, setAlertContent] = useState<string>('');

  const { fetchAndFormatFilesForDisplay } = useFileBrowserContext();
  const { currentFileSharePath } = useZoneBrowserContext();
  const { cookies } = useCookiesContext();

  async function renameItem(
    originalPath: string,
    originalPathWithoutFileName: string
  ) {
    const newPath = `${originalPathWithoutFileName}/${newName}`;
    await sendFetchRequest(
      `${getAPIPathRoot()}api/fileglancer/files/${currentFileSharePath?.name}?subpath=${originalPath}`,
      'PATCH',
      cookies['_xsrf'],
      { path: newPath }
    );
    await fetchAndFormatFilesForDisplay(
      `${currentFileSharePath?.name}?subpath=${originalPathWithoutFileName}`
    );
  }

  async function handleRenameSubmit(subpath: string) {
    setShowAlert(false);

    if (currentFileSharePath) {
      const originalPathWithoutFileName = removeLastSegmentFromPath(subpath);
      try {
        await renameItem(subpath, originalPathWithoutFileName);
        const alertContent = `Renamed item at path: ${currentFileSharePath.name}/${subpath} to ${newName}`;
        setAlertContent(alertContent);
      } catch (error) {
        const errorContent = `Error renaming item at path: ${currentFileSharePath.name}/${subpath} to ${newName}`;
        setAlertContent(
          `${errorContent}. Error details: ${error instanceof Error ? error.message : 'Unknown error'}`
        );
      }
    } else if (!currentFileSharePath) {
      setAlertContent('No file share path selected.');
    }
    setShowAlert(true);
  }

  return {
    handleRenameSubmit,
    newName,
    setNewName,
    showAlert,
    setShowAlert,
    alertContent
  };
}
