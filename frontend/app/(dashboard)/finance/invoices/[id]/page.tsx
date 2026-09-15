import { InvoiceDetail } from '@/components/finance/InvoiceDetail';

export default function InvoiceDetailPage({ params }: { params: { id: string } }) {
  return (
    <div className="p-6 max-w-7xl mx-auto">
      <InvoiceDetail invoiceId={params.id} />
    </div>
  );
}
