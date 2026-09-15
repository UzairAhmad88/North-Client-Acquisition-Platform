import { DocumentViewer } from '@/frontend/components/documents/DocumentViewer';

interface DocumentDetailPageProps {
  params: {
    id: string;
  };
}

export default function DocumentDetailPage({ params }: DocumentDetailPageProps) {
  return (
    <div className="p-6 max-w-7xl mx-auto">
      <DocumentViewer documentId={params.id} />
    </div>
  );
}
